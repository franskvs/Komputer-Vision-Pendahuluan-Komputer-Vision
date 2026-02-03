"""
=============================================================================
PRAKTIKUM 05 - SCENE RECOGNITION
=============================================================================
Program ini mendemonstrasikan Scene Recognition - klasifikasi gambar
berdasarkan scene/environment (indoor, outdoor, dll).

Konsep yang dipelajari:
1. Scene classification vs object classification
2. Places dataset dan kategorisasi scene
3. Indoor vs outdoor classification
4. Scene attributes dan semantic understanding

Scene Recognition berbeda dari Object Recognition:
- Object: Fokus pada individual objects (kucing, mobil)
- Scene: Fokus pada overall environment (dapur, pantai, kantor)

Kebutuhan:
- opencv-python >= 4.8.0
- numpy

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import os


def print_scene_recognition_concepts():
    """
    Menampilkan konsep Scene Recognition.
    """
    print("\n" + "="*70)
    print("KONSEP SCENE RECOGNITION")
    print("="*70)
    
    print("""
    [DEFINISI]
    ─────────────────────────────────────────────────────────────────────
    
    Scene Recognition: Mengklasifikasikan gambar berdasarkan 
    ENVIRONMENT atau LOKASI, bukan individual objects.
    
    Contoh:
    - Object Recognition: "Ada mobil, pohon, dan lampu jalan"
    - Scene Recognition: "Ini adalah jalan perkotaan"
    
    
    [PLACES DATASET]
    ─────────────────────────────────────────────────────────────────────
    
    Places365: Dataset benchmark untuk scene recognition
    - 365 scene categories
    - ~1.8 million training images
    - Categories mencakup indoor dan outdoor scenes
    
    Contoh categories:
    
    Indoor:
    ├── bedroom, bathroom, kitchen
    ├── office, classroom, library
    ├── restaurant, cafe, bar
    ├── hospital room, waiting room
    └── garage, basement, attic
    
    Outdoor:
    ├── beach, ocean, lake
    ├── forest, jungle, desert
    ├── street, highway, parking lot
    ├── mountain, valley, canyon
    └── farm, vineyard, garden
    
    
    [HIERARCHY OF SCENES]
    ─────────────────────────────────────────────────────────────────────
    
    Level 1: Indoor / Outdoor / Both
    
    Level 2: Functional category
    ├── Residential (bedroom, bathroom)
    ├── Commercial (office, store)
    ├── Transportation (airport, train station)
    ├── Nature (forest, beach)
    └── Urban (street, plaza)
    
    Level 3: Specific scene (365 categories)
    
    
    [SCENE ATTRIBUTES]
    ─────────────────────────────────────────────────────────────────────
    
    Selain category, scenes juga punya attributes:
    
    Spatial:
    - Open / Enclosed
    - Natural / Man-made
    - Symmetric / Asymmetric
    
    Functional:
    - Working / Relaxing
    - Social / Isolated
    - Formal / Casual
    
    Material:
    - Wood / Metal / Glass
    - Natural materials / Artificial
    """)


def get_scene_categories():
    """
    Returns scene categories untuk demonstrasi.
    """
    categories = {
        "Indoor": [
            "bedroom", "bathroom", "kitchen", "living_room", "dining_room",
            "office", "classroom", "library", "laboratory",
            "restaurant", "cafe", "bar", "hospital_room",
            "gym", "theater", "museum", "church",
            "garage", "basement", "attic", "corridor"
        ],
        "Outdoor_Natural": [
            "beach", "ocean", "lake", "river", "waterfall",
            "forest", "jungle", "rainforest", "bamboo_forest",
            "mountain", "valley", "canyon", "cliff",
            "desert", "field", "meadow", "swamp",
            "garden", "park", "farm"
        ],
        "Outdoor_Urban": [
            "street", "highway", "intersection", "crosswalk",
            "plaza", "square", "courtyard",
            "parking_lot", "gas_station",
            "bridge", "tunnel",
            "construction_site", "industrial_area",
            "residential_neighborhood", "downtown"
        ],
        "Transportation": [
            "airport_terminal", "train_station", "bus_station",
            "subway_station", "harbor", "marina",
            "airplane_cabin", "train_interior", "bus_interior"
        ]
    }
    return categories


def create_scene_image(scene_type="indoor"):
    """
    Membuat sample scene image untuk demonstrasi.
    """
    image = np.ones((300, 400, 3), dtype=np.uint8) * 200
    
    if scene_type == "indoor_bedroom":
        # Floor and ceiling
        cv2.rectangle(image, (0, 200), (400, 300), (120, 100, 80), -1)  # Floor
        cv2.rectangle(image, (0, 0), (400, 50), (240, 240, 250), -1)    # Ceiling
        
        # Walls
        cv2.rectangle(image, (0, 50), (400, 200), (220, 220, 230), -1)
        
        # Bed
        cv2.rectangle(image, (50, 130), (250, 200), (100, 80, 60), -1)  # Frame
        cv2.rectangle(image, (55, 135), (245, 195), (255, 255, 255), -1)  # Mattress
        cv2.rectangle(image, (55, 135), (100, 175), (180, 180, 200), -1)  # Pillow
        
        # Nightstand
        cv2.rectangle(image, (270, 150), (320, 200), (80, 60, 40), -1)
        
        # Lamp
        cv2.rectangle(image, (285, 120), (305, 150), (60, 60, 60), -1)  # Base
        cv2.ellipse(image, (295, 110), (20, 15), 0, 180, 360, (255, 255, 200), -1)  # Shade
        
        # Window
        cv2.rectangle(image, (300, 60), (380, 140), (50, 50, 50), 3)
        cv2.rectangle(image, (305, 65), (375, 135), (150, 200, 255), -1)
        cv2.line(image, (340, 65), (340, 135), (50, 50, 50), 2)
        cv2.line(image, (305, 100), (375, 100), (50, 50, 50), 2)
        
    elif scene_type == "outdoor_beach":
        # Sky gradient
        for y in range(150):
            blue = int(255 - y * 0.3)
            image[y, :] = [blue, 200, 255]
        
        # Ocean
        for y in range(150, 200):
            blue = int(180 - (y-150) * 0.5)
            image[y, :] = [blue + 50, blue, 50]
        
        # Sand
        cv2.rectangle(image, (0, 200), (400, 300), (130, 180, 220), -1)
        
        # Sun
        cv2.circle(image, (350, 50), 30, (100, 200, 255), -1)
        
        # Waves
        for x in range(0, 400, 30):
            pts = np.array([[x, 200], [x+15, 195], [x+30, 200]], np.int32)
            cv2.polylines(image, [pts], False, (200, 200, 100), 2)
        
        # Palm tree
        cv2.rectangle(image, (60, 120), (75, 220), (60, 80, 100), -1)  # Trunk
        # Leaves
        cv2.ellipse(image, (67, 100), (50, 20), 30, 0, 180, (50, 120, 50), -1)
        cv2.ellipse(image, (67, 100), (50, 20), -30, 0, 180, (50, 120, 50), -1)
        cv2.ellipse(image, (67, 100), (40, 15), 80, 0, 180, (60, 140, 60), -1)
        
        # Umbrella
        cv2.ellipse(image, (250, 180), (40, 20), 0, 180, 360, (80, 80, 200), -1)
        cv2.line(image, (250, 180), (250, 230), (80, 60, 40), 3)
        
    elif scene_type == "outdoor_street":
        # Sky
        cv2.rectangle(image, (0, 0), (400, 100), (255, 200, 150), -1)
        
        # Buildings
        for x, h, color in [(0, 150, (150, 150, 160)), 
                            (80, 180, (140, 140, 150)),
                            (150, 160, (160, 160, 170)),
                            (220, 200, (130, 130, 140)),
                            (300, 170, (150, 150, 160))]:
            cv2.rectangle(image, (x, 300-h), (x+75, 180), color, -1)
            # Windows
            for wy in range(300-h+10, 175, 25):
                for wx in range(x+10, x+70, 20):
                    cv2.rectangle(image, (wx, wy), (wx+10, wy+15), (200, 200, 150), -1)
        
        # Road
        cv2.rectangle(image, (0, 180), (400, 300), (60, 60, 60), -1)
        
        # Road markings
        for x in range(20, 400, 50):
            cv2.rectangle(image, (x, 235), (x+30, 245), (255, 255, 255), -1)
        
        # Sidewalk
        cv2.rectangle(image, (0, 180), (400, 200), (180, 180, 180), -1)
        
        # Street light
        cv2.rectangle(image, (350, 80), (358, 180), (50, 50, 50), -1)
        cv2.ellipse(image, (354, 75), (15, 8), 0, 0, 360, (100, 200, 255), -1)
        
    else:  # Default indoor
        # Simple room
        cv2.rectangle(image, (0, 0), (400, 300), (220, 220, 230), -1)  # Wall
        cv2.rectangle(image, (0, 200), (400, 300), (120, 100, 80), -1)  # Floor
        
        # Door
        cv2.rectangle(image, (50, 80), (130, 200), (80, 60, 40), -1)
        cv2.circle(image, (120, 145), 5, (200, 180, 50), -1)  # Handle
        
        # Window
        cv2.rectangle(image, (200, 60), (350, 150), (150, 200, 255), -1)
        cv2.line(image, (275, 60), (275, 150), (50, 50, 50), 3)
        cv2.line(image, (200, 105), (350, 105), (50, 50, 50), 3)
    
    return image


def demo_scene_classification():
    """
    Demonstrasi scene classification.
    """
    print("\n" + "="*70)
    print("SCENE CLASSIFICATION DEMO")
    print("="*70)
    
    # Create sample scenes
    scenes = [
        ("indoor_bedroom", "Bedroom"),
        ("outdoor_beach", "Beach"),
        ("outdoor_street", "Urban Street")
    ]
    
    print("\n[INFO] Generating sample scenes...")
    
    images = []
    for scene_type, label in scenes:
        img = create_scene_image(scene_type)
        images.append((img, label))
        print(f"  Created: {label}")
    
    # Simulated classification
    print("\n[CLASSIFICATION RESULTS]")
    print("-"*60)
    
    for img, true_label in images:
        # Simulated predictions
        if "bedroom" in true_label.lower():
            predictions = [
                ("bedroom", 0.82), ("hotel_room", 0.08), ("dorm_room", 0.05),
                ("living_room", 0.03), ("hospital_room", 0.02)
            ]
        elif "beach" in true_label.lower():
            predictions = [
                ("beach", 0.89), ("coast", 0.05), ("ocean", 0.03),
                ("lake", 0.02), ("resort", 0.01)
            ]
        else:
            predictions = [
                ("street", 0.75), ("downtown", 0.10), ("alley", 0.07),
                ("plaza", 0.05), ("parking_lot", 0.03)
            ]
        
        print(f"\nTrue label: {true_label}")
        print("Predictions:")
        for pred_label, prob in predictions:
            bar = "█" * int(prob * 30)
            print(f"  {pred_label:20s} {prob:.2%} {bar}")
    
    # Visualize
    display_images = []
    for img, label in images:
        img_with_label = img.copy()
        cv2.putText(img_with_label, label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img_with_label, label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
        display_images.append(img_with_label)
    
    # Stack horizontally
    combined = np.hstack(display_images)
    
    cv2.imshow("Scene Classification Demo", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_indoor_outdoor_classification():
    """
    Demonstrasi indoor vs outdoor classification.
    """
    print("\n" + "="*70)
    print("INDOOR vs OUTDOOR CLASSIFICATION")
    print("="*70)
    
    print("""
    [BINARY CLASSIFICATION]
    ─────────────────────────────────────────────────────────────────────
    
    Task: Klasifikasi gambar sebagai Indoor atau Outdoor
    
    Features yang membedakan:
    
    Indoor indicators:
    - Ceiling visible
    - Artificial lighting
    - Walls, doors, windows from inside
    - Furniture
    - Limited depth of field
    
    Outdoor indicators:
    - Sky visible
    - Natural lighting (sun, clouds)
    - Horizon line
    - Vegetation (trees, grass)
    - Extended depth of field
    """)
    
    # Create demo images
    indoor_img = create_scene_image("indoor_bedroom")
    outdoor_img = create_scene_image("outdoor_beach")
    
    # Simulated classification
    print("\n[CLASSIFICATION RESULTS]")
    print("-"*50)
    
    classifications = [
        (indoor_img, "Image 1", {"Indoor": 0.95, "Outdoor": 0.05}),
        (outdoor_img, "Image 2", {"Indoor": 0.02, "Outdoor": 0.98})
    ]
    
    for img, name, probs in classifications:
        print(f"\n{name}:")
        for label, prob in probs.items():
            bar = "█" * int(prob * 30)
            status = "✓" if prob > 0.5 else " "
            print(f"  [{status}] {label:10s} {prob:.2%} {bar}")
    
    # Visualize with labels
    indoor_display = indoor_img.copy()
    outdoor_display = outdoor_img.copy()
    
    cv2.putText(indoor_display, "INDOOR (95%)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(outdoor_display, "OUTDOOR (98%)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    combined = np.hstack([indoor_display, outdoor_display])
    
    cv2.imshow("Indoor vs Outdoor Classification", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_scene_attributes():
    """
    Demonstrasi scene attributes.
    """
    print("\n" + "="*70)
    print("SCENE ATTRIBUTES")
    print("="*70)
    
    print("""
    [SCENE ATTRIBUTES]
    ─────────────────────────────────────────────────────────────────────
    
    Selain category, scenes bisa described dengan attributes:
    """)
    
    attributes = {
        "Spatial Layout": [
            "open_area", "enclosed", "cluttered", "sparse",
            "symmetric", "natural", "man-made"
        ],
        "Materials": [
            "wood", "metal", "glass", "stone", "fabric",
            "vegetation", "water"
        ],
        "Functions": [
            "relaxing", "working", "socializing", "traveling",
            "shopping", "dining", "sleeping"
        ],
        "Lighting": [
            "natural_light", "artificial_light", "dim", "bright",
            "sunny", "cloudy"
        ],
        "Weather (outdoor)": [
            "sunny", "cloudy", "rainy", "snowy", "foggy"
        ]
    }
    
    for category, attrs in attributes.items():
        print(f"\n{category}:")
        print(f"  {', '.join(attrs)}")
    
    # Demo attribute prediction
    print("\n[ATTRIBUTE PREDICTION DEMO]")
    print("-"*50)
    
    scene_examples = [
        {
            "scene": "Beach",
            "attributes": {
                "open_area": 0.95, "natural": 0.98, "sunny": 0.85,
                "water": 0.92, "relaxing": 0.88, "bright": 0.90
            }
        },
        {
            "scene": "Office",
            "attributes": {
                "enclosed": 0.90, "man-made": 0.98, "artificial_light": 0.85,
                "working": 0.95, "sparse": 0.65, "bright": 0.75
            }
        }
    ]
    
    for example in scene_examples:
        print(f"\nScene: {example['scene']}")
        print("Predicted attributes:")
        for attr, prob in example['attributes'].items():
            bar = "█" * int(prob * 20)
            status = "✓" if prob > 0.5 else " "
            print(f"  [{status}] {attr:20s} {prob:.2%} {bar}")


def demo_scene_understanding():
    """
    Demonstrasi holistic scene understanding.
    """
    print("\n" + "="*70)
    print("HOLISTIC SCENE UNDERSTANDING")
    print("="*70)
    
    print("""
    [LEVELS OF SCENE UNDERSTANDING]
    ─────────────────────────────────────────────────────────────────────
    
    Level 1: Scene Category
             "This is a beach"
    
    Level 2: Scene Attributes
             "Open, natural, sunny, relaxing"
    
    Level 3: Object Detection
             "Contains: person, umbrella, palm tree, ocean"
    
    Level 4: Spatial Relationships
             "Person is sitting under umbrella"
             "Palm tree is on the left side"
             "Ocean is in the background"
    
    Level 5: Activities/Events
             "People are relaxing on vacation"
             "It's a sunny summer day"
    
    Level 6: Semantic Understanding
             "This is a tropical resort beach"
             "The scene suggests leisure and tourism"
    
    
    [COMBINED ANALYSIS EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    """)
    
    # Comprehensive scene analysis
    analysis = {
        "Scene Category": "beach (92%)",
        "Indoor/Outdoor": "outdoor (99%)",
        "Attributes": ["open", "natural", "bright", "sunny", "relaxing"],
        "Detected Objects": [
            "sand (background)",
            "ocean (background)",
            "palm tree (left)",
            "beach umbrella (center)",
            "sun (sky)"
        ],
        "Scene Description": "A sunny tropical beach with a palm tree and umbrella, "
                           "typical of a vacation resort setting."
    }
    
    print("Image: Beach scene")
    print("-"*50)
    
    for key, value in analysis.items():
        if isinstance(value, list):
            print(f"\n{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"\n{key}: {value}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM SCENE RECOGNITION")
    print("="*70)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Konsep Scene Recognition")
        print("2. Scene Classification Demo")
        print("3. Indoor vs Outdoor Classification")
        print("4. Scene Attributes")
        print("5. Holistic Scene Understanding")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-6): ").strip()
        
        if choice == '1':
            print_scene_recognition_concepts()
        elif choice == '2':
            demo_scene_classification()
        elif choice == '3':
            demo_indoor_outdoor_classification()
        elif choice == '4':
            demo_scene_attributes()
        elif choice == '5':
            demo_scene_understanding()
        elif choice == '6':
            print_scene_recognition_concepts()
            demo_scene_classification()
            demo_indoor_outdoor_classification()
            demo_scene_attributes()
            demo_scene_understanding()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
