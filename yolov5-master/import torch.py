import torch
    
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', best.pt) 
predictions = model("Test/620.jpg")

results = model("Test/620.jpg")
labels, cord_thres = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
