function submitData() {
  const inputElement = document.getElementById("inputField");
  if (!inputElement) {
      console.error("Input field not found!");
      return;
  }

  const inputText = inputElement.value.trim();
  if (inputText === "") {
      alert("Please enter some text.");
      return;
  }

  // 發送 POST 請求
  fetch('http://192.168.0.205:8000/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ inputData: inputText })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // 假設返回的是 JSON
  })
  .then(data => {
      // 在這裡跳轉到新的頁面
      window.location.href = "http://192.168.0.205:8000/submit"; // 修改為你希望跳轉的頁面 URL
  })
  .catch(error => {
      alert("An error occurred: " + error.message);
  });
}

function selectData(event) {
  // 獲取觸發事件的按鈕
  const button = event.target;

  // 找到按鈕所在的父級 .playlist-card 元素
  const playlistCard = button.closest('.playlist-card');

  if (!playlistCard) {
      console.error("Playlist card not found!");
      return;
  }

  // 提取對應的 <h2> 元素中的文本內容
  const playlistTitleElement = playlistCard.querySelector('h2');
  if (!playlistTitleElement) {
      console.error("Playlist title not found!");
      return;
  }

  const playlistTitle = playlistTitleElement.textContent.trim();
  console.log("Selected Playlist Title:", playlistTitle);

  // 發送數據到後端（例如 POST 請求）
  fetch('http://192.168.0.205:8000/submit', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: playlistTitle })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.text(); // 假設後端返回的是一個文本響應
  })
  .then(data => {
      console.log("Server response:", data);

      // 跳轉到新的頁面
      window.location.href = "http://192.168.0.205:8000/show";
  })
  .catch(error => {
      console.error("An error occurred:", error.message);
  });
}
