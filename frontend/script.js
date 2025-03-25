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
            alert("Error: " + data.error);
            console.error("Error:", data.error);
        } else {
            // Hiển thị ảnh đã tải lên
            let uploadedImage = document.getElementById("uploadedImage");
            uploadedImage.src = data.image;
            uploadedImage.style.display = "block";

            // Hiển thị bảng kết quả
            let resultTable = document.getElementById("resultTable");
            let tbody = resultTable.querySelector("tbody");
            tbody.innerHTML = ""; // Xóa kết quả cũ nếu có

            data.predictions.forEach((item, index) => {
                let row = tbody.insertRow();
                row.insertCell(0).innerText = index + 1;
                row.insertCell(1).innerText = item.label;
                row.insertCell(2).innerText = (item.confidence * 100).toFixed(2) + "%";
            });

            resultTable.style.display = "block";
        }
    })
    .catch(error => console.error("Error:", error));
}