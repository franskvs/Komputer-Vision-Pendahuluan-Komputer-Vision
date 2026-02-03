"""
=============================================================================
PRAKTIKUM 11 - ONNX EXPORT DAN DEPLOYMENT
=============================================================================
Program ini mendemonstrasikan cara mengekspor model deep learning ke format
ONNX untuk deployment lintas platform.

Konsep yang dipelajari:
1. Apa itu ONNX dan mengapa penting
2. Export model PyTorch ke ONNX
3. Export model Keras/TensorFlow ke ONNX
4. Validasi dan optimasi ONNX model
5. Inference menggunakan ONNX Runtime

Kebutuhan:
- onnx (pip install onnx)
- onnxruntime (pip install onnxruntime)
- torch >= 2.0.0 (opsional)
- tensorflow >= 2.10.0 (opsional)
- tf2onnx (pip install tf2onnx)

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import numpy as np
import time
import os

# Check available libraries
ONNX_AVAILABLE = False
ONNXRUNTIME_AVAILABLE = False
TORCH_AVAILABLE = False
TF_AVAILABLE = False

try:
    import onnx
    from onnx import numpy_helper
    ONNX_AVAILABLE = True
    print("[INFO] ONNX tersedia")
except ImportError:
    print("[WARNING] ONNX tidak tersedia")

try:
    import onnxruntime as ort
    ONNXRUNTIME_AVAILABLE = True
    print("[INFO] ONNX Runtime tersedia")
except ImportError:
    print("[WARNING] ONNX Runtime tidak tersedia")

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
    print("[INFO] PyTorch tersedia")
except ImportError:
    print("[WARNING] PyTorch tidak tersedia")

try:
    import tensorflow as tf
    TF_AVAILABLE = True
    print("[INFO] TensorFlow tersedia")
except ImportError:
    print("[WARNING] TensorFlow tidak tersedia")


def demo_onnx_overview():
    """
    Overview tentang ONNX dan pentingnya untuk deployment.
    """
    print("\n" + "="*70)
    print("ONNX OVERVIEW")
    print("="*70)
    
    print("""
    [APA ITU ONNX?]
    ─────────────────────────────────────────────────────────────────────
    ONNX = Open Neural Network Exchange
    
    - Format open untuk merepresentasikan model machine learning
    - Memungkinkan interoperability antar framework
    - Dikembangkan oleh Microsoft, Facebook, Amazon, dll
    
    
    [MENGAPA ONNX PENTING?]
    ─────────────────────────────────────────────────────────────────────
    
    1. PORTABILITY
       ─────────────
       Train di PyTorch → Deploy di TensorRT, CoreML, OpenVINO
       
       PyTorch ──┐
       TensorFlow┼──► ONNX ──► TensorRT (NVIDIA GPU)
       Keras ────┤           ├► OpenVINO (Intel CPU)
       Scikit ───┘           ├► CoreML (Apple devices)
                             └► ONNX Runtime (Cross-platform)
    
    2. OPTIMIZATION
       ─────────────
       - ONNX Runtime melakukan graph optimization
       - Hardware-specific acceleration
       - Quantization support (FP16, INT8)
    
    3. DEPLOYMENT FLEXIBILITY
       ──────────────────────
       - Server (Linux, Windows)
       - Mobile (iOS, Android)
       - Edge devices (Raspberry Pi, Jetson)
       - Web (ONNX.js, WebAssembly)
    
    
    [ONNX STRUCTURE]
    ─────────────────────────────────────────────────────────────────────
    
    ONNX Model terdiri dari:
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                         ONNX Model                              │
    ├─────────────────────────────────────────────────────────────────┤
    │  ┌─────────────────┐                                            │
    │  │ Model Metadata  │ → IR version, producer name, opset version │
    │  └─────────────────┘                                            │
    │                                                                 │
    │  ┌─────────────────┐                                            │
    │  │     Graph       │ → Computational graph                      │
    │  │  ┌───────────┐  │                                            │
    │  │  │  Inputs   │  │ → Input tensor definitions                 │
    │  │  ├───────────┤  │                                            │
    │  │  │  Outputs  │  │ → Output tensor definitions                │
    │  │  ├───────────┤  │                                            │
    │  │  │   Nodes   │  │ → Operations (Conv, ReLU, etc.)            │
    │  │  ├───────────┤  │                                            │
    │  │  │Initializers│ │ → Weights and biases                       │
    │  │  └───────────┘  │                                            │
    │  └─────────────────┘                                            │
    └─────────────────────────────────────────────────────────────────┘
    
    
    [ONNX OPSET VERSION]
    ─────────────────────────────────────────────────────────────────────
    
    Opset version menentukan operator yang tersedia:
    
    ┌─────────┬───────────────────────────────────────────────────────┐
    │ Version │ Key Features                                          │
    ├─────────┼───────────────────────────────────────────────────────┤
    │  7-9    │ Basic ops, limited dynamic shapes                     │
    │  10-11  │ Better RNN support, more ops                          │
    │  12-13  │ Training support, dynamic shapes improved             │
    │  14-15  │ Transformer support, more activations                 │
    │  16-17  │ Better quantization, GridSample                       │
    │  18+    │ Latest ops, BiasAdd, LpPool                          │
    └─────────┴───────────────────────────────────────────────────────┘
    
    Tip: Use opset 13+ for modern models, 11+ for compatibility
    """)


def demo_pytorch_to_onnx():
    """
    Demonstrasi export model PyTorch ke ONNX.
    """
    print("\n" + "="*70)
    print("PYTORCH TO ONNX EXPORT")
    print("="*70)
    
    if not TORCH_AVAILABLE:
        print("\n[WARNING] PyTorch tidak tersedia - menampilkan panduan")
        print("""
    [CARA EXPORT PYTORCH KE ONNX]
    ─────────────────────────────────────────────────────────────────────
    
    import torch
    
    # 1. Define model
    class SimpleModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = torch.nn.Conv2d(3, 32, 3, padding=1)
            self.relu = torch.nn.ReLU()
            self.pool = torch.nn.AdaptiveAvgPool2d(1)
            self.fc = torch.nn.Linear(32, 10)
        
        def forward(self, x):
            x = self.relu(self.conv1(x))
            x = self.pool(x).flatten(1)
            return self.fc(x)
    
    # 2. Create model and dummy input
    model = SimpleModel()
    model.eval()
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # 3. Export to ONNX
    torch.onnx.export(
        model,
        dummy_input,
        "model.onnx",
        export_params=True,         # Store trained weights
        opset_version=13,           # ONNX opset version
        do_constant_folding=True,   # Optimization
        input_names=['input'],      # Input name
        output_names=['output'],    # Output name
        dynamic_axes={              # Dynamic batch size
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print("Model exported to model.onnx")
        """)
        return
    
    print("\n[INFO] Creating and exporting PyTorch model...")
    
    # Define simple model
    class SimpleClassifier(nn.Module):
        """Simple CNN classifier for demonstration."""
        def __init__(self, num_classes=10):
            super(SimpleClassifier, self).__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 32, 3, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),
                nn.Conv2d(32, 64, 3, padding=1),
                nn.BatchNorm2d(64),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),
            )
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
            self.classifier = nn.Linear(64, num_classes)
        
        def forward(self, x):
            x = self.features(x)
            x = self.avgpool(x)
            x = torch.flatten(x, 1)
            x = self.classifier(x)
            return x
    
    # Create model
    model = SimpleClassifier(num_classes=10)
    model.eval()
    
    # Print model summary
    total_params = sum(p.numel() for p in model.parameters())
    print(f"[INFO] Model parameters: {total_params:,}")
    
    # Create dummy input
    batch_size = 1
    dummy_input = torch.randn(batch_size, 3, 64, 64)
    
    # Test forward pass
    with torch.no_grad():
        output = model(dummy_input)
    print(f"[INFO] Input shape: {dummy_input.shape}")
    print(f"[INFO] Output shape: {output.shape}")
    
    # Export to ONNX
    onnx_path = "simple_classifier.onnx"
    
    print(f"\n[INFO] Exporting to {onnx_path}...")
    
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=13,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        },
        verbose=False
    )
    
    print(f"[INFO] Model exported successfully!")
    print(f"[INFO] File size: {os.path.getsize(onnx_path) / 1024:.2f} KB")
    
    # Verify ONNX model
    if ONNX_AVAILABLE:
        print("\n[INFO] Verifying ONNX model...")
        onnx_model = onnx.load(onnx_path)
        onnx.checker.check_model(onnx_model)
        print("[INFO] ONNX model verified successfully!")
        
        # Print model info
        print(f"\n[INFO] Model IR version: {onnx_model.ir_version}")
        print(f"[INFO] Opset version: {onnx_model.opset_import[0].version}")
        print(f"[INFO] Producer: {onnx_model.producer_name}")
        
        # Print inputs and outputs
        print("\n[INFO] Model inputs:")
        for input in onnx_model.graph.input:
            print(f"  - {input.name}: {[d.dim_value for d in input.type.tensor_type.shape.dim]}")
        
        print("[INFO] Model outputs:")
        for output in onnx_model.graph.output:
            print(f"  - {output.name}: {[d.dim_value for d in output.type.tensor_type.shape.dim]}")


def demo_keras_to_onnx():
    """
    Demonstrasi export model Keras ke ONNX.
    """
    print("\n" + "="*70)
    print("KERAS/TENSORFLOW TO ONNX EXPORT")
    print("="*70)
    
    if not TF_AVAILABLE:
        print("\n[WARNING] TensorFlow tidak tersedia - menampilkan panduan")
        print("""
    [CARA EXPORT KERAS/TENSORFLOW KE ONNX]
    ─────────────────────────────────────────────────────────────────────
    
    # Method 1: Using tf2onnx command line
    # ─────────────────────────────────────
    
    # Save Keras model as SavedModel
    model.save('saved_model')
    
    # Convert using tf2onnx
    # python -m tf2onnx.convert --saved-model saved_model --output model.onnx
    
    
    # Method 2: Using tf2onnx Python API
    # ───────────────────────────────────
    
    import tf2onnx
    import tensorflow as tf
    
    # Create Keras model
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10)
    ])
    
    # Convert to ONNX
    input_signature = [tf.TensorSpec([None, 224, 224, 3], tf.float32, name='input')]
    
    onnx_model, _ = tf2onnx.convert.from_keras(
        model,
        input_signature=input_signature,
        opset=13
    )
    
    # Save
    with open('model.onnx', 'wb') as f:
        f.write(onnx_model.SerializeToString())
        """)
        return
    
    print("\n[INFO] Creating and exporting Keras model...")
    
    # Create simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same',
                               input_shape=(64, 64, 3)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10)
    ])
    
    model.summary()
    
    # Test forward pass
    dummy_input = np.random.randn(1, 64, 64, 3).astype(np.float32)
    output = model(dummy_input)
    print(f"\n[INFO] Input shape: {dummy_input.shape}")
    print(f"[INFO] Output shape: {output.shape}")
    
    # Try to export using tf2onnx
    try:
        import tf2onnx
        
        print("\n[INFO] Exporting to ONNX using tf2onnx...")
        
        input_signature = [tf.TensorSpec([None, 64, 64, 3], tf.float32, name='input')]
        
        onnx_model, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=input_signature,
            opset=13
        )
        
        onnx_path = "keras_model.onnx"
        with open(onnx_path, 'wb') as f:
            f.write(onnx_model.SerializeToString())
        
        print(f"[INFO] Model exported to {onnx_path}")
        print(f"[INFO] File size: {os.path.getsize(onnx_path) / 1024:.2f} KB")
        
    except ImportError:
        print("\n[WARNING] tf2onnx not installed. Install with: pip install tf2onnx")
        print("[INFO] Alternatively, save as SavedModel and convert via CLI:")
        print("       python -m tf2onnx.convert --saved-model ./saved_model --output model.onnx")


def demo_onnx_inference():
    """
    Demonstrasi inference menggunakan ONNX Runtime.
    """
    print("\n" + "="*70)
    print("ONNX RUNTIME INFERENCE")
    print("="*70)
    
    print("""
    [ONNX RUNTIME OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    
    ONNX Runtime adalah high-performance inference engine untuk ONNX models.
    
    Features:
    - Cross-platform (Windows, Linux, macOS, iOS, Android)
    - Hardware acceleration (CPU, GPU, NPU)
    - Optimizations (graph, hardware-specific)
    - Language bindings (Python, C++, C#, Java, JavaScript)
    
    
    [EXECUTION PROVIDERS]
    ─────────────────────────────────────────────────────────────────────
    
    ┌──────────────────┬───────────────────────────────────────────────┐
    │ Provider         │ Description                                   │
    ├──────────────────┼───────────────────────────────────────────────┤
    │ CPUExecutionProvider    │ Default CPU inference                  │
    │ CUDAExecutionProvider   │ NVIDIA GPU with CUDA                   │
    │ TensorRTExecutionProvider│ NVIDIA TensorRT optimization          │
    │ OpenVINOExecutionProvider│ Intel hardware (CPU, iGPU)            │
    │ CoreMLExecutionProvider │ Apple Neural Engine                    │
    │ DirectMLExecutionProvider│ Windows DirectX 12 GPU                │
    │ ROCMExecutionProvider   │ AMD GPU                                │
    │ QNNExecutionProvider    │ Qualcomm NPU                           │
    └──────────────────┴───────────────────────────────────────────────┘
    """)
    
    if not ONNXRUNTIME_AVAILABLE:
        print("\n[WARNING] ONNX Runtime tidak tersedia")
        print("[INFO] Install dengan: pip install onnxruntime")
        print("[INFO] Untuk GPU: pip install onnxruntime-gpu")
        return
    
    # Check for existing ONNX model or create synthetic
    onnx_path = "simple_classifier.onnx"
    
    if not os.path.exists(onnx_path):
        if TORCH_AVAILABLE and ONNX_AVAILABLE:
            print("\n[INFO] Creating ONNX model for demo...")
            demo_pytorch_to_onnx()
        else:
            print("\n[WARNING] No ONNX model available for inference demo")
            print("[INFO] Create a model first using demo_pytorch_to_onnx()")
            return
    
    print("\n[INFO] Loading ONNX model with ONNX Runtime...")
    
    # Check available providers
    providers = ort.get_available_providers()
    print(f"[INFO] Available execution providers: {providers}")
    
    # Create inference session
    session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    
    # Get input/output info
    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    input_type = session.get_inputs()[0].type
    
    output_name = session.get_outputs()[0].name
    output_shape = session.get_outputs()[0].shape
    
    print(f"\n[INFO] Input: {input_name}")
    print(f"  - Shape: {input_shape}")
    print(f"  - Type: {input_type}")
    
    print(f"[INFO] Output: {output_name}")
    print(f"  - Shape: {output_shape}")
    
    # Create test input
    batch_size = 1
    # Determine input size (handle dynamic batch)
    if isinstance(input_shape[0], str) or input_shape[0] is None:
        input_shape = [batch_size] + list(input_shape[1:])
    
    test_input = np.random.randn(*input_shape).astype(np.float32)
    print(f"\n[INFO] Test input shape: {test_input.shape}")
    
    # Run inference
    print("[INFO] Running inference...")
    
    # Warmup
    for _ in range(3):
        _ = session.run([output_name], {input_name: test_input})
    
    # Benchmark
    num_runs = 100
    times = []
    
    for _ in range(num_runs):
        start = time.time()
        outputs = session.run([output_name], {input_name: test_input})
        times.append(time.time() - start)
    
    avg_time = np.mean(times) * 1000
    std_time = np.std(times) * 1000
    
    print(f"\n[BENCHMARK RESULTS]")
    print(f"  - Average inference time: {avg_time:.2f} ms")
    print(f"  - Std deviation: {std_time:.2f} ms")
    print(f"  - Throughput: {1000/avg_time:.1f} FPS")
    
    # Output info
    print(f"\n[INFO] Output shape: {outputs[0].shape}")
    print(f"[INFO] Output sample: {outputs[0][0][:5]}...")
    
    # Batch inference demo
    print("\n[INFO] Testing batch inference...")
    
    batch_sizes = [1, 2, 4, 8, 16]
    
    for bs in batch_sizes:
        try:
            batch_input = np.random.randn(bs, *input_shape[1:]).astype(np.float32)
            
            start = time.time()
            for _ in range(10):
                _ = session.run([output_name], {input_name: batch_input})
            avg_time = (time.time() - start) / 10 * 1000
            
            print(f"  Batch size {bs:2d}: {avg_time:.2f} ms ({bs*1000/avg_time:.1f} samples/sec)")
        except Exception as e:
            print(f"  Batch size {bs:2d}: Failed - {e}")


def demo_onnx_optimization():
    """
    Demonstrasi optimasi model ONNX.
    """
    print("\n" + "="*70)
    print("ONNX MODEL OPTIMIZATION")
    print("="*70)
    
    print("""
    [OPTIMIZATION TECHNIQUES]
    ─────────────────────────────────────────────────────────────────────
    
    1. GRAPH OPTIMIZATION (ONNX Runtime)
       ──────────────────────────────────
       - Constant folding
       - Redundant node elimination
       - Operator fusion (Conv+BN, MatMul+Add, etc.)
       
       Levels:
       - ORT_DISABLE_ALL: No optimization
       - ORT_ENABLE_BASIC: Basic optimization
       - ORT_ENABLE_EXTENDED: Extended optimization
       - ORT_ENABLE_ALL: All optimizations
    
    2. QUANTIZATION
       ─────────────
       - Float32 → Float16 (FP16)
       - Float32 → INT8
       - Dynamic quantization
       - Static quantization (requires calibration)
    
    3. ONNX SIMPLIFIER
       ────────────────
       - Removes unnecessary nodes
       - Simplifies graph structure
       - pip install onnx-simplifier
    
    4. HARDWARE-SPECIFIC
       ──────────────────
       - TensorRT for NVIDIA GPU
       - OpenVINO for Intel
       - CoreML for Apple
    """)
    
    if not ONNXRUNTIME_AVAILABLE:
        print("\n[WARNING] ONNX Runtime tidak tersedia untuk demo optimisasi")
        return
    
    onnx_path = "simple_classifier.onnx"
    
    if not os.path.exists(onnx_path):
        print(f"\n[WARNING] {onnx_path} tidak ditemukan")
        print("[INFO] Jalankan demo_pytorch_to_onnx() terlebih dahulu")
        return
    
    print("\n[INFO] Testing different optimization levels...")
    
    # Test different optimization levels
    opt_levels = [
        ('Disabled', ort.GraphOptimizationLevel.ORT_DISABLE_ALL),
        ('Basic', ort.GraphOptimizationLevel.ORT_ENABLE_BASIC),
        ('Extended', ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED),
        ('All', ort.GraphOptimizationLevel.ORT_ENABLE_ALL),
    ]
    
    results = []
    
    for name, level in opt_levels:
        # Create session options
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = level
        
        # Create session
        session = ort.InferenceSession(
            onnx_path, 
            sess_options,
            providers=['CPUExecutionProvider']
        )
        
        # Get input info
        input_name = session.get_inputs()[0].name
        input_shape = session.get_inputs()[0].shape
        output_name = session.get_outputs()[0].name
        
        # Handle dynamic batch
        if isinstance(input_shape[0], str) or input_shape[0] is None:
            input_shape = [1] + list(input_shape[1:])
        
        test_input = np.random.randn(*input_shape).astype(np.float32)
        
        # Warmup
        for _ in range(5):
            _ = session.run([output_name], {input_name: test_input})
        
        # Benchmark
        times = []
        for _ in range(50):
            start = time.time()
            _ = session.run([output_name], {input_name: test_input})
            times.append(time.time() - start)
        
        avg_time = np.mean(times) * 1000
        results.append((name, avg_time))
        
        print(f"  {name:10s}: {avg_time:.3f} ms")
    
    # Quantization demo
    print("\n[INFO] Quantization options:")
    print("""
    # Dynamic quantization (easiest)
    from onnxruntime.quantization import quantize_dynamic, QuantType
    
    quantize_dynamic(
        model_input='model.onnx',
        model_output='model_quantized.onnx',
        weight_type=QuantType.QUInt8
    )
    
    # Static quantization (better accuracy, needs calibration data)
    from onnxruntime.quantization import quantize_static, CalibrationDataReader
    
    class MyCalibrationDataReader(CalibrationDataReader):
        def __init__(self, calibration_data):
            self.data = calibration_data
            self.iter = iter(self.data)
        
        def get_next(self):
            try:
                return {'input': next(self.iter)}
            except StopIteration:
                return None
    
    quantize_static(
        model_input='model.onnx',
        model_output='model_static_quantized.onnx',
        calibration_data_reader=MyCalibrationDataReader(data)
    )
    """)


def demo_onnx_visualization():
    """
    Demonstrasi visualisasi model ONNX.
    """
    print("\n" + "="*70)
    print("ONNX MODEL VISUALIZATION")
    print("="*70)
    
    print("""
    [VISUALIZATION TOOLS]
    ─────────────────────────────────────────────────────────────────────
    
    1. NETRON (Recommended)
       ─────────────────────
       - Web: https://netron.app/
       - Desktop app: pip install netron
       - Run: netron model.onnx
    
    2. ONNX IN PYTHON
       ────────────────
       - Print model structure
       - Analyze operators
       - Check inputs/outputs
    
    3. TENSORBOARD
       ─────────────
       - Convert ONNX to TensorBoard format
       - Visualize graph
    """)
    
    if not ONNX_AVAILABLE:
        print("\n[WARNING] ONNX tidak tersedia untuk analisis model")
        return
    
    onnx_path = "simple_classifier.onnx"
    
    if not os.path.exists(onnx_path):
        print(f"\n[WARNING] {onnx_path} tidak ditemukan")
        return
    
    print(f"\n[INFO] Analyzing {onnx_path}...")
    
    # Load model
    model = onnx.load(onnx_path)
    
    # Basic info
    print("\n[MODEL INFO]")
    print(f"  IR Version: {model.ir_version}")
    print(f"  Opset Version: {model.opset_import[0].version}")
    print(f"  Producer: {model.producer_name} {model.producer_version}")
    
    # Inputs
    print("\n[INPUTS]")
    for input in model.graph.input:
        shape = [d.dim_value if d.dim_value else d.dim_param 
                 for d in input.type.tensor_type.shape.dim]
        print(f"  {input.name}: {shape}")
    
    # Outputs
    print("\n[OUTPUTS]")
    for output in model.graph.output:
        shape = [d.dim_value if d.dim_value else d.dim_param
                 for d in output.type.tensor_type.shape.dim]
        print(f"  {output.name}: {shape}")
    
    # Count operators
    print("\n[OPERATORS]")
    op_counts = {}
    for node in model.graph.node:
        op_type = node.op_type
        op_counts[op_type] = op_counts.get(op_type, 0) + 1
    
    for op, count in sorted(op_counts.items()):
        print(f"  {op}: {count}")
    
    print(f"\nTotal nodes: {len(model.graph.node)}")
    
    # Count parameters
    total_params = 0
    print("\n[INITIALIZERS (Weights)]")
    for init in model.graph.initializer[:5]:  # Show first 5
        arr = numpy_helper.to_array(init)
        params = arr.size
        total_params += params
        print(f"  {init.name}: {arr.shape} ({params:,} params)")
    
    if len(model.graph.initializer) > 5:
        print(f"  ... and {len(model.graph.initializer) - 5} more")
        for init in model.graph.initializer[5:]:
            arr = numpy_helper.to_array(init)
            total_params += arr.size
    
    print(f"\nTotal parameters: {total_params:,}")
    
    # How to visualize with Netron
    print("\n[VISUALIZE WITH NETRON]")
    print("  Option 1: Open https://netron.app/ and upload the file")
    print(f"  Option 2: Run 'netron {onnx_path}' in terminal")
    print("  Option 3: Import in Python:")
    print("    import netron")
    print(f"    netron.start('{onnx_path}')")


def demo_deployment_patterns():
    """
    Demonstrasi pola deployment untuk ONNX models.
    """
    print("\n" + "="*70)
    print("DEPLOYMENT PATTERNS")
    print("="*70)
    
    print("""
    [DEPLOYMENT SCENARIOS]
    ─────────────────────────────────────────────────────────────────────
    
    1. SERVER DEPLOYMENT
       ──────────────────
       
       ┌─────────────┐    ┌─────────────────────────────────────┐
       │   Client    │───►│          Server                     │
       │ (REST API)  │◄───│  FastAPI/Flask + ONNX Runtime       │
       └─────────────┘    │  ├── Load model on startup          │
                          │  ├── Batch requests                 │
                          │  └── Return predictions             │
                          └─────────────────────────────────────┘
       
       Example (FastAPI):
       ```python
       from fastapi import FastAPI
       import onnxruntime as ort
       import numpy as np
       
       app = FastAPI()
       session = ort.InferenceSession("model.onnx")
       
       @app.post("/predict")
       async def predict(data: dict):
           input_data = np.array(data["input"]).astype(np.float32)
           output = session.run(None, {"input": input_data})
           return {"prediction": output[0].tolist()}
       ```
    
    2. EDGE DEPLOYMENT (Raspberry Pi, Jetson)
       ──────────────────────────────────────
       
       - Use lightweight models (MobileNet, EfficientNet-Lite)
       - Quantize to INT8 for better performance
       - Consider ONNX Runtime Mobile or TensorFlow Lite
       
       Optimization tips:
       - Reduce input resolution
       - Use batch size 1
       - Enable hardware acceleration (CUDA, NPU)
    
    3. MOBILE DEPLOYMENT (iOS/Android)
       ────────────────────────────────
       
       iOS:
       - Convert ONNX → CoreML using coremltools
       - Use Vision framework for preprocessing
       
       Android:
       - Use ONNX Runtime Android
       - Or convert to TensorFlow Lite
    
    4. WEB DEPLOYMENT (Browser)
       ────────────────────────
       
       Options:
       - ONNX Runtime Web (WebAssembly)
       - TensorFlow.js
       
       ```javascript
       // ONNX Runtime Web
       const session = await ort.InferenceSession.create('model.onnx');
       const input = new ort.Tensor('float32', data, [1, 3, 224, 224]);
       const output = await session.run({ input: input });
       ```
    
    
    [DEPLOYMENT CHECKLIST]
    ─────────────────────────────────────────────────────────────────────
    
    □ Model exported and validated
    □ Input/output shapes documented
    □ Preprocessing pipeline defined
    □ Postprocessing (softmax, NMS) implemented
    □ Performance benchmarked
    □ Memory usage measured
    □ Error handling implemented
    □ Logging and monitoring set up
    □ Model versioning strategy defined
    □ A/B testing framework ready (if needed)
    
    
    [BEST PRACTICES]
    ─────────────────────────────────────────────────────────────────────
    
    1. PREPROCESSING
       - Match training preprocessing exactly
       - Handle different input sizes
       - Normalize inputs consistently
    
    2. BATCHING
       - Implement request batching for throughput
       - Consider dynamic batching
    
    3. CACHING
       - Cache model in memory
       - Consider prediction caching for common inputs
    
    4. MONITORING
       - Log inference times
       - Track prediction distribution
       - Set up alerts for anomalies
    
    5. VERSIONING
       - Track model versions
       - Support rollback
       - Document changes
    """)


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM ONNX EXPORT DAN DEPLOYMENT")
    print("="*70)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. ONNX Overview")
        print("2. PyTorch to ONNX Export")
        print("3. Keras to ONNX Export")
        print("4. ONNX Runtime Inference")
        print("5. ONNX Model Optimization")
        print("6. ONNX Model Visualization")
        print("7. Deployment Patterns")
        print("8. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-8): ").strip()
        
        if choice == '1':
            demo_onnx_overview()
        elif choice == '2':
            demo_pytorch_to_onnx()
        elif choice == '3':
            demo_keras_to_onnx()
        elif choice == '4':
            demo_onnx_inference()
        elif choice == '5':
            demo_onnx_optimization()
        elif choice == '6':
            demo_onnx_visualization()
        elif choice == '7':
            demo_deployment_patterns()
        elif choice == '8':
            demo_onnx_overview()
            demo_pytorch_to_onnx()
            demo_keras_to_onnx()
            demo_onnx_inference()
            demo_onnx_optimization()
            demo_onnx_visualization()
            demo_deployment_patterns()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
