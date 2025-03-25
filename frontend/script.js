document.addEventListener("DOMContentLoaded", function() {
    // Xử lý hiển thị menu đăng xuất
    const userInfo = document.querySelector(".user-info");
    const logoutMenu = document.getElementById("logout-menu");

    userInfo.addEventListener("click", function(event) {
        logoutMenu.style.display = logoutMenu.style.display === "block" ? "none" : "block";
        event.stopPropagation(); // Ngăn chặn sự kiện lan ra ngoài
    });

    // Ẩn menu đăng xuất khi nhấn ra ngoài
    document.addEventListener("click", function(event) {
        if (!userInfo.contains(event.target)) {
            logoutMenu.style.display = "none";
        }
    });

    // Xử lý tải và hiển thị ảnh
    document.getElementById("imageUpload").addEventListener("change", function() {
        let file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function(e) {
                let uploadedImage = document.getElementById("uploadedImage");
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // Gửi ảnh lên server để nhận diện
    window.uploadImage = function() {
        let fileInput = document.getElementById("imageUpload").files[0];
        if (!fileInput) {
            alert("Vui lòng chọn ảnh!");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput);

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Lỗi: " + data.error);
                console.error("Lỗi:", data.error);
            } else {
                let tbody = document.querySelector("#resultTable tbody");
                tbody.innerHTML = "";
                data.predictions.forEach((item, index) => {
                    let row = tbody.insertRow();
                    row.insertCell(0).innerText = index + 1;
                    row.insertCell(1).innerText = item.label;
                    row.insertCell(2).innerText = (item.confidence * 100).toFixed(2) + "%";
                });
                document.getElementById("resultTable").style.display = "block";
            }
        })
        .catch(error => console.error("Lỗi:", error));
    };
});