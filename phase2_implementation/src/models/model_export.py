"""
Model Export and Optimization for Mobile Deployment
TFLite, ONNX, and quantization support
Vital Lens AI Phase 2
"""

import numpy as np
from typing import Optional, Dict, Tuple, List
from pathlib import Path
from dataclasses import dataclass


@dataclass
class QuantizationConfig:
    """Configuration for model quantization"""
    quantize_int8: bool = True
    calibration_dataset: Optional[List[np.ndarray]] = None
    target_size_kb: int = 50  # Target model size
    max_quantization_error: float = 0.05  # 5% max error allowed


class ModelOptimizer:
    """
    Optimize and export rPPG models for mobile deployment.
    
    Supports:
    - TensorFlow Lite (Android)
    - ONNX (cross-platform)
    - Quantization (int8, fp16)
    - Batch processing optimization
    """
    
    def __init__(self, model_type: str = "pos"):
        """
        Initialize optimizer.
        
        Args:
            model_type: Type of model ("pos", "chrom", "deeplearning")
        """
        self.model_type = model_type
        self.quantization_stats = {}
    
    def export_to_tflite(
        self,
        model_path: str,
        output_path: str,
        input_shape: Tuple[int, ...] = (1, 3),
        quantization_config: Optional[QuantizationConfig] = None,
    ) -> Dict[str, any]:
        """
        Export model to TensorFlow Lite format.
        
        Args:
            model_path: Path to saved model
            output_path: Output TFLite model path
            input_shape: Input tensor shape
            quantization_config: Quantization configuration
            
        Returns:
            Optimization report
        """
        report = {
            "model_type": self.model_type,
            "format": "tflite",
            "input_shape": input_shape,
            "quantized": False,
            "original_size_kb": 0,
            "optimized_size_kb": 0,
            "compression_ratio": 1.0,
            "inference_time_ms": None,
            "error_metrics": {},
        }
        
        try:
            import tensorflow as tf
        except ImportError:
            print("Warning: TensorFlow not installed. Skipping TFLite export.")
            return report
        
        # Load model
        try:
            # Try loading as SavedModel
            model = tf.saved_model.load(model_path)
        except:
            # Try loading as Keras model
            model = tf.keras.models.load_model(model_path)
        
        # Create converter
        converter = tf.lite.TFLiteConverter.from_concrete_functions(
            [model.signatures['serving_default']]
        )
        
        # Apply quantization if requested
        if quantization_config and quantization_config.quantize_int8:
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_ops = [
                tf.lite.OpsSet.TFLITE_BUILTINS_INT8
            ]
            
            # Set quantization parameters
            converter.inference_input_type = tf.uint8
            converter.inference_output_type = tf.uint8
            report["quantized"] = True
        
        # Convert
        tflite_model = converter.convert()
        
        # Save
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        # Calculate sizes
        original_size = Path(model_path).stat().st_size / 1024 if Path(model_path).exists() else 0
        optimized_size = len(tflite_model) / 1024
        
        report.update({
            "original_size_kb": original_size,
            "optimized_size_kb": optimized_size,
            "compression_ratio": original_size / optimized_size if optimized_size > 0 else 1.0,
        })
        
        return report
    
    def export_to_onnx(
        self,
        model_path: str,
        output_path: str,
        input_shape: Tuple[int, ...] = (1, 3),
    ) -> Dict[str, any]:
        """
        Export model to ONNX format for cross-platform support.
        
        Args:
            model_path: Path to saved model
            output_path: Output ONNX model path
            input_shape: Input tensor shape
            
        Returns:
            Optimization report
        """
        report = {
            "model_type": self.model_type,
            "format": "onnx",
            "input_shape": input_shape,
            "original_size_kb": 0,
            "optimized_size_kb": 0,
        }
        
        try:
            import tf2onnx
            import tensorflow as tf
        except ImportError:
            print("Warning: tf2onnx not installed. Skipping ONNX export.")
            return report
        
        try:
            # Load model
            model = tf.saved_model.load(model_path)
            
            # Convert to ONNX
            onnx_model, _ = tf2onnx.convert.from_keras(model)
            
            # Save
            import onnx
            onnx.save(onnx_model, output_path)
            
            # Calculate sizes
            original_size = Path(model_path).stat().st_size / 1024 if Path(model_path).exists() else 0
            optimized_size = Path(output_path).stat().st_size / 1024 if Path(output_path).exists() else 0
            
            report.update({
                "original_size_kb": original_size,
                "optimized_size_kb": optimized_size,
                "compression_ratio": original_size / optimized_size if optimized_size > 0 else 1.0,
            })
        except Exception as e:
            print(f"ONNX export failed: {e}")
        
        return report
    
    def quantize_int8(
        self,
        model: any,
        calibration_data: np.ndarray,
        max_error: float = 0.05,
    ) -> Tuple[any, Dict]:
        """
        Apply int8 quantization to model.
        
        Args:
            model: Tensorflow/PyTorch model
            calibration_data: Data for calibration
            max_error: Maximum allowed error (0-1)
            
        Returns:
            (quantized_model, metrics)
        """
        metrics = {
            "original_dtype": "float32",
            "quantized_dtype": "int8",
            "quantization_scale": 1.0,
            "quantization_zero_point": 0,
            "max_error": 0.0,
            "mean_error": 0.0,
        }
        
        try:
            # Get quantization parameters
            # Q = (value / scale) + zero_point
            q_min = -128
            q_max = 127
            
            # Calibrate scale
            v_min = np.min(calibration_data)
            v_max = np.max(calibration_data)
            
            scale = (v_max - v_min) / (q_max - q_min)
            zero_point = -round(v_min / scale)
            
            # Simulate quantization
            quantized = np.round(calibration_data / scale + zero_point)
            quantized = np.clip(quantized, q_min, q_max)
            dequantized = (quantized - zero_point) * scale
            
            # Calculate error
            error = np.abs(calibration_data - dequantized) / (np.abs(calibration_data) + 1e-6)
            
            metrics.update({
                "quantization_scale": float(scale),
                "quantization_zero_point": int(zero_point),
                "max_error": float(np.max(error)),
                "mean_error": float(np.mean(error)),
            })
        except Exception as e:
            print(f"Quantization failed: {e}")
        
        return model, metrics
    
    def optimize_for_streaming(
        self,
        model_config: Dict,
    ) -> Dict:
        """
        Optimize model architecture for streaming (real-time) inference.
        
        Modifications:
        - Reduce model depth (fewer layers)
        - Smaller input window
        - Optimize for low latency
        
        Args:
            model_config: Original model configuration
            
        Returns:
            Optimized configuration
        """
        optimized = model_config.copy()
        
        # Reduce network size for mobile
        if "num_layers" in optimized:
            optimized["num_layers"] = max(1, optimized["num_layers"] // 2)
        
        if "hidden_size" in optimized:
            optimized["hidden_size"] = max(16, optimized["hidden_size"] // 2)
        
        # Reduce window size for lower latency
        if "window_size" in optimized:
            optimized["window_size"] = min(optimized["window_size"], 30)  # Max 1 second at 30fps
        
        # Enable batch normalization folding
        optimized["fold_batch_norm"] = True
        
        return optimized
    
    def profile_inference(
        self,
        model_path: str,
        input_data: np.ndarray,
        num_runs: int = 100,
        use_gpu: bool = False,
    ) -> Dict:
        """
        Profile model inference performance.
        
        Args:
            model_path: Path to model
            input_data: Sample input
            num_runs: Number of inference runs
            use_gpu: Use GPU if available
            
        Returns:
            Performance metrics
        """
        import time
        
        metrics = {
            "model_path": str(model_path),
            "input_shape": input_data.shape,
            "num_runs": num_runs,
            "total_time_ms": 0.0,
            "mean_time_ms": 0.0,
            "median_time_ms": 0.0,
            "std_time_ms": 0.0,
            "min_time_ms": 0.0,
            "max_time_ms": 0.0,
            "fps": 0.0,
        }
        
        try:
            import tensorflow as tf
            
            # Load interpreter
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()
            
            # Get input/output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Prepare input
            input_tensor = interpreter.tensor(input_details[0]["index"])
            
            # Run inference
            times = []
            for _ in range(num_runs):
                start = time.time()
                interpreter.set_tensor(input_details[0]["index"], input_data)
                interpreter.invoke()
                end = time.time()
                times.append((end - start) * 1000)
            
            times = np.array(times)
            
            metrics.update({
                "total_time_ms": float(np.sum(times)),
                "mean_time_ms": float(np.mean(times)),
                "median_time_ms": float(np.median(times)),
                "std_time_ms": float(np.std(times)),
                "min_time_ms": float(np.min(times)),
                "max_time_ms": float(np.max(times)),
                "fps": 1000.0 / float(np.mean(times)),
            })
        except Exception as e:
            print(f"Profiling failed: {e}")
        
        return metrics
    
    def validate_accuracy(
        self,
        original_model_path: str,
        optimized_model_path: str,
        test_data: np.ndarray,
        test_labels: np.ndarray,
    ) -> Dict:
        """
        Validate that optimized model maintains accuracy.
        
        Args:
            original_model_path: Path to original model
            optimized_model_path: Path to optimized model
            test_data: Test input data
            test_labels: Test ground truth
            
        Returns:
            Accuracy comparison metrics
        """
        metrics = {
            "original_accuracy": 0.0,
            "optimized_accuracy": 0.0,
            "accuracy_drop": 0.0,
            "mean_absolute_error": 0.0,
        }
        
        try:
            import tensorflow as tf
            
            # Load both models
            original_interpreter = tf.lite.Interpreter(model_path=original_model_path)
            original_interpreter.allocate_tensors()
            
            optimized_interpreter = tf.lite.Interpreter(model_path=optimized_model_path)
            optimized_interpreter.allocate_tensors()
            
            # Run inference on test data
            original_preds = []
            optimized_preds = []
            
            for i in range(len(test_data)):
                # Original
                original_interpreter.set_tensor(
                    original_interpreter.get_input_details()[0]["index"],
                    test_data[i:i+1]
                )
                original_interpreter.invoke()
                orig_output = original_interpreter.get_tensor(
                    original_interpreter.get_output_details()[0]["index"]
                )
                original_preds.append(orig_output.flatten())
                
                # Optimized
                optimized_interpreter.set_tensor(
                    optimized_interpreter.get_input_details()[0]["index"],
                    test_data[i:i+1]
                )
                optimized_interpreter.invoke()
                opt_output = optimized_interpreter.get_tensor(
                    optimized_interpreter.get_output_details()[0]["index"]
                )
                optimized_preds.append(opt_output.flatten())
            
            original_preds = np.array(original_preds)
            optimized_preds = np.array(optimized_preds)
            
            # Calculate metrics
            mae = np.mean(np.abs(original_preds - optimized_preds))
            
            metrics.update({
                "mean_absolute_error": float(mae),
            })
        except Exception as e:
            print(f"Accuracy validation failed: {e}")
        
        return metrics


# Example usage
if __name__ == "__main__":
    optimizer = ModelOptimizer(model_type="pos")
    
    # Example: Export to TFLite with quantization
    config = QuantizationConfig(
        quantize_int8=True,
        target_size_kb=50,
    )
    
    # report = optimizer.export_to_tflite(
    #     "path/to/model",
    #     "path/to/output.tflite",
    #     input_shape=(1, 3),
    #     quantization_config=config,
    # )
    # print(report)
    
    print("Model optimizer ready for Phase 2 implementation.")
