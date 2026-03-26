def diagnose_blobs(images):
    print("=== Blob Diagnostic ===\n")
    for x, img in enumerate(images):
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"Image {x}: {len(contours)} total blobs")
        
        areas = []
        circularities = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 10:
                continue
            perimeter = cv2.arcLength(contour, True)
            circularity = (4 * np.pi * area / (perimeter ** 2)) if perimeter > 0 else 0
            areas.append(area)
            circularities.append(circularity)
        
        if areas:
            print(f"  Area     — min: {min(areas):.0f}  max: {max(areas):.0f}  median: {np.median(areas):.0f}")
            print(f"  Circular — min: {min(circularities):.3f}  max: {max(circularities):.3f}  median: {np.median(circularities):.3f}")
            
            # Show how many blobs fall into each bucket
            small  = sum(1 for a in areas if a < MIN_VESSEL_AREA)
            medium = sum(1 for a in areas if MIN_VESSEL_AREA <= a <= MAX_VESSEL_AREA)
            large  = sum(1 for a in areas if a > MAX_VESSEL_AREA)
            circ   = sum(1 for c in circularities if c >= CIRCULARITY_THRESHOLD)
            
            print(f"  Blobs below MIN_VESSEL_AREA ({MIN_VESSEL_AREA}):   {small}")
            print(f"  Blobs in vessel area range:                {medium}")
            print(f"  Blobs above MAX_VESSEL_AREA ({MAX_VESSEL_AREA}): {large}")
            print(f"  Blobs above circularity threshold ({CIRCULARITY_THRESHOLD}): {circ}")
        print()

diagnose_blobs(images)