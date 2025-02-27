from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
import cv2
import os
import pickle

def extract_features(image_patch):
    """Extract features from component image patch"""
    # Resize to standard size
    resized = cv2.resize(image_patch, (64, 64))
    
    # Extract HOG features (Histogram of Oriented Gradients)
    winSize = (64, 64)
    blockSize = (16, 16)
    blockStride = (8, 8)
    cellSize = (8, 8)
    nbins = 9
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    features = hog.compute(resized)
    
    # Add shape features
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h if h > 0 else 0
        
        shape_features = np.array([area, perimeter, aspect_ratio])
        return np.concatenate([features.flatten(), shape_features])
    
    return features.flatten()

def train_component_classifier(data_dir):
    """Train a component classifier from labeled images"""
    X = []  # Features
    y = []  # Labels
    
    # Load labeled data
    for component_type in os.listdir(data_dir):
        type_dir = os.path.join(data_dir, component_type)
        if os.path.isdir(type_dir):
            for img_file in os.listdir(type_dir):
                if img_file.endswith(('.png', '.jpg')):
                    img_path = os.path.join(type_dir, img_file)
                    img = cv2.imread(img_path)
                    if img is not None:
                        features = extract_features(img)
                        X.append(features)
                        y.append(component_type)
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Train SVM classifier
    clf = SVC(kernel='rbf', probability=True)
    clf.fit(X_train, y_train)
    
    # Evaluate
    accuracy = clf.score(X_test, y_test)
    print(f"Classifier accuracy: {accuracy:.2f}")
    
    # Save model
    model_data = {
        'classifier': clf,
        'scaler': scaler
    }
    with open('component_classifier.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    return model_data

# Example usage:
# train_component_classifier('labeled_components')