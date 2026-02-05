"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 04 - CNN DENGAN KERAS/TENSORFLOW
# Assignment - set nilai ke variabel
=============================================================================
Program ini membangun dan melatih CNN menggunakan Keras/TensorFlow.
Keras menyediakan API high-level yang lebih mudah untuk prototyping.

Konsep yang dipelajari:
1. Sequential dan Functional API Keras
2. Layer types (Conv2D, MaxPooling2D, Dense, Dropout)
3. Model compilation (optimizer, loss, metrics)
4. Callbacks (EarlyStopping, ModelCheckpoint)
5. Training history visualization

Kebutuhan:
# Assignment - set nilai ke variabel
- tensorflow >= 2.10.0 (includes Keras)
- numpy
- matplotlib

Note: Jika TensorFlow tidak tersedia, program akan menjalankan simulasi.

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import os

# Check apakah TensorFlow tersedia
TENSORFLOW_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import tensorflow as tf
    # Import library/module untuk digunakan
    from tensorflow import keras
    # Import library/module untuk digunakan
    from tensorflow.keras import layers, models
    # Import library/module untuk digunakan
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    # Assignment - set nilai ke variabel
    TENSORFLOW_AVAILABLE = True
    print(f"[INFO] TensorFlow version: {tf.__version__}")
    print("[INFO] TensorFlow tersedia - menggunakan real implementation")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] TensorFlow tidak tersedia - menggunakan simulasi")


# Definisi function dengan nama dan parameter
def build_cnn_sequential():
    """
    Membangun CNN menggunakan Sequential API.
    
    Sequential API cocok untuk model linear (layer-by-layer)
    tanpa branching atau multiple inputs/outputs.
    
    Returns:
        keras.Model: CNN model
    """
    # Conditional statement - eksekusi jika kondisi True
    if not TENSORFLOW_AVAILABLE:
        # Return value dari function
        return None
    
    # Assignment - set nilai ke variabel
    model = keras.Sequential([
        # Input layer (implisit dari input_shape di layer pertama)
        
        # Block 1: Conv + Pool
        layers.Conv2D(32, (3, 3), activation='relu', 
                     # Assignment - set nilai ke variabel
                     input_shape=(28, 28, 1), padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Block 2: Conv + Pool
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Block 3: Conv
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        
        # Classifier head
        layers.Flatten(),
        layers.Dropout(0.5),
        # Assignment - set nilai ke variabel
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        # Assignment - set nilai ke variabel
        layers.Dense(10, activation='softmax')
    ])
    
    # Return value dari function
    return model


# Definisi function dengan nama dan parameter
def build_cnn_functional():
    """
    Membangun CNN menggunakan Functional API.
    
    Functional API lebih fleksibel untuk:
    - Multi-input/multi-output models
    - Models dengan shared layers
    - Non-linear topology (residual connections)
    
    Returns:
        keras.Model: CNN model
    """
    # Conditional statement - eksekusi jika kondisi True
    if not TENSORFLOW_AVAILABLE:
        # Return value dari function
        return None
    
    # Input layer
    inputs = keras.Input(shape=(28, 28, 1), name='input_image')
    
    # Block 1
    x = layers.Conv2D(32, (3, 3), padding='same', name='conv1')(inputs)
    # Assignment - set nilai ke variabel
    x = layers.BatchNormalization(name='bn1')(x)
    # Assignment - set nilai ke variabel
    x = layers.Activation('relu', name='relu1')(x)
    # Assignment - set nilai ke variabel
    x = layers.MaxPooling2D((2, 2), name='pool1')(x)
    
    # Block 2
    x = layers.Conv2D(64, (3, 3), padding='same', name='conv2')(x)
    # Assignment - set nilai ke variabel
    x = layers.BatchNormalization(name='bn2')(x)
    # Assignment - set nilai ke variabel
    x = layers.Activation('relu', name='relu2')(x)
    # Assignment - set nilai ke variabel
    x = layers.MaxPooling2D((2, 2), name='pool2')(x)
    
    # Block 3
    x = layers.Conv2D(64, (3, 3), padding='same', name='conv3')(x)
    # Assignment - set nilai ke variabel
    x = layers.BatchNormalization(name='bn3')(x)
    # Assignment - set nilai ke variabel
    x = layers.Activation('relu', name='relu3')(x)
    
    # Classifier
    x = layers.GlobalAveragePooling2D(name='gap')(x)
    # Assignment - set nilai ke variabel
    x = layers.Dropout(0.5, name='dropout1')(x)
    # Assignment - set nilai ke variabel
    x = layers.Dense(128, activation='relu', name='fc1')(x)
    # Assignment - set nilai ke variabel
    x = layers.Dropout(0.3, name='dropout2')(x)
    # Assignment - set nilai ke variabel
    outputs = layers.Dense(10, activation='softmax', name='predictions')(x)
    
    # Create model
    model = keras.Model(inputs=inputs, outputs=outputs, name='CNN_Functional')
    
    # Return value dari function
    return model


# Definisi function dengan nama dan parameter
def demo_model_building():
    """
    Demonstrasi membangun model dengan Keras.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("MEMBANGUN MODEL CNN DENGAN KERAS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Conditional statement - eksekusi jika kondisi True
    if TENSORFLOW_AVAILABLE:
        # Build models
        print("\n[1] Sequential API Model:")
        print("-"*50)
        # Assignment - set nilai ke variabel
        model_seq = build_cnn_sequential()
        model_seq.summary()
        
        print("\n[2] Functional API Model:")
        print("-"*50)
        # Assignment - set nilai ke variabel
        model_func = build_cnn_functional()
        model_func.summary()
        
    else:
        print("\n[SIMULASI] Model Architecture")
        print("-"*50)
        print("""
        Model: "sequential"
        _________________________________________________________________
         Layer (type)                Output Shape              Param #   
        # Assignment - set nilai ke variabel
        =================================================================
         conv2d (Conv2D)             (None, 28, 28, 32)        320       
         batch_normalization         (None, 28, 28, 32)        128       
         max_pooling2d               (None, 14, 14, 32)        0         
         conv2d_1 (Conv2D)           (None, 14, 14, 64)        18496     
         batch_normalization_1       (None, 14, 14, 64)        256       
         max_pooling2d_1             (None, 7, 7, 64)          0         
         conv2d_2 (Conv2D)           (None, 7, 7, 64)          36928     
         batch_normalization_2       (None, 7, 7, 64)          256       
         flatten (Flatten)           (None, 3136)              0         
         dropout (Dropout)           (None, 3136)              0         
         dense (Dense)               (None, 128)               401536    
         batch_normalization_3       (None, 128)               512       
         dropout_1 (Dropout)         (None, 128)               0         
         dense_1 (Dense)             (None, 10)                1290      
        # Assignment - set nilai ke variabel
        =================================================================
        Total params: 459,722
        Trainable params: 459,146
        Non-trainable params: 576
        _________________________________________________________________
        """)


# Definisi function dengan nama dan parameter
def demo_compilation():
    """
    Demonstrasi model compilation dengan berbagai optimizer dan loss.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("MODEL COMPILATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Model Compilation Components:
    
    1. OPTIMIZER - Algoritma untuk update weights
    ─────────────────────────────────────────────────────────────────────
    
    a) SGD (Stochastic Gradient Descent)
       - Sederhana, reliable
       - Bisa lambat converge
       
       # Assignment - set nilai ke variabel
       optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)
    
    b) Adam (Adaptive Moment Estimation)
       - Default choice, works well out-of-box
       - Combines momentum + RMSprop
       
       # Assignment - set nilai ke variabel
       optimizer = keras.optimizers.Adam(learning_rate=0.001)
    
    c) RMSprop
       - Good untuk RNN dan noisy gradients
       
       # Assignment - set nilai ke variabel
       optimizer = keras.optimizers.RMSprop(learning_rate=0.001)
    
    
    2. LOSS FUNCTION - Mengukur error
    ─────────────────────────────────────────────────────────────────────
    
    a) CategoricalCrossentropy
       # Definisi class untuk membuat object
       - Untuk multi-class dengan one-hot labels
       
       # Assignment - set nilai ke variabel
       loss = 'categorical_crossentropy'
    
    b) SparseCategoricalCrossentropy
       # Definisi class untuk membuat object
       - Untuk multi-class dengan integer labels
       
       # Assignment - set nilai ke variabel
       loss = 'sparse_categorical_crossentropy'
    
    c) BinaryCrossentropy
       - Untuk binary classification
       
       # Assignment - set nilai ke variabel
       loss = 'binary_crossentropy'
    
    
    3. METRICS - Untuk monitoring
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    metrics = ['accuracy', 'precision', 'recall', 'AUC']
    
    
    [CODE EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    
    model.compile(
        # Assignment - set nilai ke variabel
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        # Assignment - set nilai ke variabel
        loss='sparse_categorical_crossentropy',
        # Assignment - set nilai ke variabel
        metrics=['accuracy']
    )
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TENSORFLOW_AVAILABLE:
        # Assignment - set nilai ke variabel
        model = build_cnn_sequential()
        model.compile(
            # Assignment - set nilai ke variabel
            optimizer='adam',
            # Assignment - set nilai ke variabel
            loss='sparse_categorical_crossentropy',
            # Assignment - set nilai ke variabel
            metrics=['accuracy']
        )
        print("\n[INFO] Model compiled successfully!")
        print(f"  Optimizer: {model.optimizer.__class__.__name__}")
        print(f"  Loss: {model.loss}")
        print(f"  Metrics: {model.metrics_names}")


# Definisi function dengan nama dan parameter
def demo_callbacks():
    """
    Demonstrasi penggunaan callbacks untuk training.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("CALLBACKS UNTUK TRAINING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Callbacks - fungsi yang dijalankan pada event tertentu
    
    1. EarlyStopping
    ─────────────────────────────────────────────────────────────────────
    Menghentikan training jika metric tidak improve.
    
    # Assignment - set nilai ke variabel
    early_stop = EarlyStopping(
        # Assignment - set nilai ke variabel
        monitor='val_loss',      # Metric yang dimonitor
        # Assignment - set nilai ke variabel
        patience=5,              # Epochs tanpa improvement sebelum stop
        # Assignment - set nilai ke variabel
        restore_best_weights=True # Restore weights terbaik
    )
    
    
    2. ModelCheckpoint
    ─────────────────────────────────────────────────────────────────────
    Menyimpan model pada interval tertentu.
    
    # Assignment - set nilai ke variabel
    checkpoint = ModelCheckpoint(
        'best_model.h5',
        # Assignment - set nilai ke variabel
        monitor='val_accuracy',
        # Assignment - set nilai ke variabel
        save_best_only=True,     # Hanya simpan jika improve
        # Assignment - set nilai ke variabel
        mode='max'               # 'max' untuk accuracy, 'min' untuk loss
    )
    
    
    3. ReduceLROnPlateau
    ─────────────────────────────────────────────────────────────────────
    Mengurangi learning rate jika training stuck.
    
    # Assignment - set nilai ke variabel
    reduce_lr = ReduceLROnPlateau(
        # Assignment - set nilai ke variabel
        monitor='val_loss',
        # Assignment - set nilai ke variabel
        factor=0.2,              # LR = LR * factor
        # Assignment - set nilai ke variabel
        patience=3,              # Epochs sebelum reduce
        # Assignment - set nilai ke variabel
        min_lr=1e-6
    )
    
    
    4. TensorBoard
    ─────────────────────────────────────────────────────────────────────
    Logging untuk visualisasi di TensorBoard.
    
    # Assignment - set nilai ke variabel
    tensorboard = TensorBoard(
        # Assignment - set nilai ke variabel
        log_dir='./logs',
        # Assignment - set nilai ke variabel
        histogram_freq=1
    )
    
    
    [USAGE]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    callbacks = [early_stop, checkpoint, reduce_lr, tensorboard]
    
    # Train model dengan data training dan validation
    model.fit(
        x_train, y_train,
        # Assignment - set nilai ke variabel
        validation_data=(x_val, y_val),
        # Assignment - set nilai ke variabel
        epochs=100,
        # Assignment - set nilai ke variabel
        callbacks=callbacks
    )
    """)


# Definisi function dengan nama dan parameter
def demo_training_keras():
    """
    Demonstrasi training lengkap dengan Keras.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("TRAINING CNN DENGAN KERAS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Conditional statement - eksekusi jika kondisi True
    if not TENSORFLOW_AVAILABLE:
        print("[WARNING] TensorFlow tidak tersedia, menjalankan simulasi...")
        demo_training_simulation()
        return
    
    # Load MNIST dataset
    print("\n[INFO] Loading MNIST dataset...")
    # Assignment - set nilai ke variabel
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Preprocessing
    # 1. Normalize ke [0, 1]
    x_train = x_train.astype('float32') / 255.0
    # Assignment - set nilai ke variabel
    x_test = x_test.astype('float32') / 255.0
    
    # 2. Reshape untuk channel dimension
    x_train = x_train.reshape(-1, 28, 28, 1)
    # Assignment - set nilai ke variabel
    x_test = x_test.reshape(-1, 28, 28, 1)
    
    print(f"[INFO] Training data shape: {x_train.shape}")
    print(f"[INFO] Test data shape: {x_test.shape}")
    
    # Build model
    print("\n[INFO] Building model...")
    # Assignment - set nilai ke variabel
    model = build_cnn_sequential()
    
    # Compile
    model.compile(
        # Assignment - set nilai ke variabel
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        # Assignment - set nilai ke variabel
        loss='sparse_categorical_crossentropy',
        # Assignment - set nilai ke variabel
        metrics=['accuracy']
    )
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            # Assignment - set nilai ke variabel
            monitor='val_loss',
            # Assignment - set nilai ke variabel
            patience=3,
            # Assignment - set nilai ke variabel
            restore_best_weights=True,
            # Assignment - set nilai ke variabel
            verbose=1
        ),
        ReduceLROnPlateau(
            # Assignment - set nilai ke variabel
            monitor='val_loss',
            # Assignment - set nilai ke variabel
            factor=0.5,
            # Assignment - set nilai ke variabel
            patience=2,
            # Assignment - set nilai ke variabel
            min_lr=1e-6,
            # Assignment - set nilai ke variabel
            verbose=1
        )
    ]
    
    # Training
    print("\n[INFO] Starting training...")
    print("-"*60)
    
    # Train model dengan data training dan validation
    history = model.fit(
        x_train, y_train,
        # Assignment - set nilai ke variabel
        validation_split=0.1,
        # Assignment - set nilai ke variabel
        epochs=10,
        # Assignment - set nilai ke variabel
        batch_size=64,
        # Assignment - set nilai ke variabel
        callbacks=callbacks,
        # Assignment - set nilai ke variabel
        verbose=1
    )
    
    # Evaluation
    print("\n[INFO] Evaluating on test set...")
    # Assignment - set nilai ke variabel
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"\n[RESULT] Test Loss: {test_loss:.4f}")
    print(f"[RESULT] Test Accuracy: {test_accuracy:.4f}")
    
    # Save model
    model.save('mnist_cnn_keras.h5')
    print("\n[INFO] Model saved to mnist_cnn_keras.h5")
    
    # Plot training history
    print("\n[INFO] Training History:")
    print("-"*60)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch, (loss, acc, val_loss, val_acc) in enumerate(zip(
        history.history['loss'],
        history.history['accuracy'],
        history.history['val_loss'],
        history.history['val_accuracy']
    ), 1):
        # Assignment - set nilai ke variabel
        print(f"Epoch {epoch}: loss={loss:.4f}, acc={acc:.4f}, "
              # Assignment - set nilai ke variabel
              f"val_loss={val_loss:.4f}, val_acc={val_acc:.4f}")


# Definisi function dengan nama dan parameter
def demo_training_simulation():
    """
    Simulasi training Keras tanpa TensorFlow.
    """
    print("\n[SIMULASI] Training CNN dengan Keras")
    print("-"*60)
    
    # Assignment - set nilai ke variabel
    simulated_history = {
        'loss': [0.5234, 0.1523, 0.0923, 0.0678, 0.0512, 0.0423],
        'accuracy': [0.8234, 0.9512, 0.9712, 0.9789, 0.9834, 0.9867],
        'val_loss': [0.2345, 0.1234, 0.0856, 0.0734, 0.0689, 0.0712],
        'val_accuracy': [0.9234, 0.9623, 0.9734, 0.9778, 0.9801, 0.9789]
    }
    
    print("\nTraining Progress:")
    print("-"*60)
    print(f"{'Epoch':<8} {'Loss':<10} {'Acc':<10} {'Val Loss':<10} {'Val Acc':<10}")
    print("-"*60)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch in range(len(simulated_history['loss'])):
        print(f"{epoch+1:<8} "
              f"{simulated_history['loss'][epoch]:<10.4f} "
              f"{simulated_history['accuracy'][epoch]:<10.4f} "
              f"{simulated_history['val_loss'][epoch]:<10.4f} "
              f"{simulated_history['val_accuracy'][epoch]:<10.4f}")
    
    print("-"*60)
    print("\n[RESULT] Simulated Test Accuracy: 98.01%")
    
    # ASCII visualization
    print("\n[TRAINING CURVES]")
    print("Loss:")
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch, loss in enumerate(simulated_history['loss'], 1):
        # Assignment - set nilai ke variabel
        bar = "█" * int((1 - loss) * 40)
        print(f"  Epoch {epoch}: {bar} {loss:.4f}")
    
    print("\nAccuracy:")
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch, acc in enumerate(simulated_history['accuracy'], 1):
        # Assignment - set nilai ke variabel
        bar = "█" * int(acc * 40)
        print(f"  Epoch {epoch}: {bar} {acc:.4f}")


# Definisi function dengan nama dan parameter
def demo_data_augmentation():
    """
    Demonstrasi data augmentation dengan Keras.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DATA AUGMENTATION DENGAN KERAS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Data Augmentation - meningkatkan variasi data training
    
    Manfaat:
    - Mengurangi overfitting
    - Meningkatkan generalization
    - Artifisial memperbesar dataset
    
    
    [KERAS LAYERS UNTUK AUGMENTATION]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    data_augmentation = keras.Sequential([
        # Rotasi random
        layers.RandomRotation(0.1),
        
        # Zoom random
        layers.RandomZoom(0.1),
        
        # Flip horizontal
        layers.RandomFlip("horizontal"),
        
        # Translation
        layers.RandomTranslation(0.1, 0.1),
        
        # Contrast adjustment
        layers.RandomContrast(0.1),
        
        # Brightness adjustment
        layers.RandomBrightness(0.1),
    ])
    
    
    [INTEGRATION DALAM MODEL]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    model = keras.Sequential([
        # Augmentation sebagai layer pertama
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        
        # Model layers
        layers.Conv2D(32, (3, 3), activation='relu'),
        ...
    ])
    
    Atau:
    
    # Augmentation terpisah, apply saat training
    augmented_data = data_augmentation(training_images)
    
    
    [IMAGEDATAGENERATOR (LEGACY)]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    datagen = ImageDataGenerator(
        # Assignment - set nilai ke variabel
        rotation_range=20,
        # Assignment - set nilai ke variabel
        width_shift_range=0.1,
        # Assignment - set nilai ke variabel
        height_shift_range=0.1,
        # Assignment - set nilai ke variabel
        horizontal_flip=True,
        # Assignment - set nilai ke variabel
        zoom_range=0.1,
        # Assignment - set nilai ke variabel
        fill_mode='nearest'
    )
    
    # Training dengan generator
    model.fit(
        # Assignment - set nilai ke variabel
        datagen.flow(x_train, y_train, batch_size=32),
        # Assignment - set nilai ke variabel
        epochs=50
    )
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TENSORFLOW_AVAILABLE:
        print("\n[DEMO] Augmentation layers")
        print("-"*50)
        
        # Create augmentation pipeline
        augmentation = keras.Sequential([
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.1, 0.1),
        # Assignment - set nilai ke variabel
        ], name="data_augmentation")
        
        # Assignment - set nilai ke variabel
        augmentation.build(input_shape=(None, 28, 28, 1))
        augmentation.summary()
        
        # Demo dengan dummy image
        print("\n[INFO] Testing augmentation...")
        # Assignment - set nilai ke variabel
        dummy_image = np.random.rand(1, 28, 28, 1).astype('float32')
        # Assignment - set nilai ke variabel
        augmented = augmentation(dummy_image, training=True)
        print(f"Input shape: {dummy_image.shape}")
        print(f"Output shape: {augmented.shape}")
        print("[INFO] Augmentation applied successfully!")


# Definisi function dengan nama dan parameter
def demo_transfer_learning_preview():
    """
    Preview konsep transfer learning dengan Keras.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("PREVIEW: TRANSFER LEARNING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Transfer Learning - memanfaatkan knowledge dari pre-trained model
    
    [WORKFLOW]
    ─────────────────────────────────────────────────────────────────────
    
    1. Load pre-trained model (tanpa classifier head)
       
       # Assignment - set nilai ke variabel
       base_model = keras.applications.MobileNetV2(
           # Assignment - set nilai ke variabel
           input_shape=(224, 224, 3),
           # Assignment - set nilai ke variabel
           include_top=False,      # Tanpa classifier
           # Assignment - set nilai ke variabel
           weights='imagenet'      # Pre-trained weights
       )
    
    2. Freeze base model weights
       
       # Assignment - set nilai ke variabel
       base_model.trainable = False
    
    3. Tambahkan custom classifier
       
       # Assignment - set nilai ke variabel
       model = keras.Sequential([
           base_model,
           layers.GlobalAveragePooling2D(),
           # Assignment - set nilai ke variabel
           layers.Dense(256, activation='relu'),
           layers.Dropout(0.5),
           # Assignment - set nilai ke variabel
           layers.Dense(num_classes, activation='softmax')
       ])
    
    4. Training (hanya classifier)
       
       model.compile(...)
       # Train model dengan data training dan validation
       model.fit(x_train, y_train, epochs=10)
    
    5. Fine-tuning (optional, unfreeze some layers)
       
       # Assignment - set nilai ke variabel
       base_model.trainable = True
       # Freeze semua kecuali beberapa layer terakhir
       for layer in base_model.layers[:-20]:
           # Assignment - set nilai ke variabel
           layer.trainable = False
       
       # Recompile dengan learning rate kecil
       model.compile(
           # Assignment - set nilai ke variabel
           optimizer=keras.optimizers.Adam(1e-5),
           ...
       )
       # Train model dengan data training dan validation
       model.fit(x_train, y_train, epochs=5)
    
    
    [AVAILABLE PRE-TRAINED MODELS]
    ─────────────────────────────────────────────────────────────────────
    
    keras.applications:
    ├── MobileNetV2, MobileNetV3
    ├── ResNet50, ResNet101, ResNet152
    ├── VGG16, VGG19
    ├── InceptionV3, InceptionResNetV2
    ├── EfficientNetB0 - B7
    ├── DenseNet121, DenseNet169, DenseNet201
    └── NASNetMobile, NASNetLarge
    """)


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM CNN DENGAN KERAS/TENSORFLOW")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Model Building (Sequential & Functional API)")
        print("2. Model Compilation")
        print("3. Callbacks")
        print("4. Training CNN")
        print("5. Data Augmentation")
        print("6. Transfer Learning Preview")
        print("7. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-7): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_model_building()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_compilation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_callbacks()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_training_keras()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_data_augmentation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_transfer_learning_preview()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '7':
            demo_model_building()
            demo_compilation()
            demo_callbacks()
            demo_training_keras()
            demo_data_augmentation()
            demo_transfer_learning_preview()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
