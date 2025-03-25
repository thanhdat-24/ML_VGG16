function uploadImage() {
    let fileInput = document.getElementById("imageUpload").files[0];
    if (!fileInput) {
        alert("Please select an image!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    console.log("Uploading image...");

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerText = "Error: " + data.error;
            console.error("Error:", data.error);
        } else {
            document.getElementById("result").innerText = "Prediction: " + data.prediction + " (Confidence: " + (data.confidence * 100).toFixed(2) + "%)";
            console.log("Prediction:", data.prediction, "Confidence:", data.confidence);
        }
    })
    .catch(error => console.error("Error:", error));
}