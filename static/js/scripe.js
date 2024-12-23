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

    fetch('/generate_subsite', {
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
        return response.text();
    })
    .then(html => {
        console.log("HTML received:", html);
        document.body.innerHTML = html; 
    })
    .catch(error => {
        alert("An error occurred: " + error.message);
    });
}

function selectData(event) {
    const button = event.target;
    const text = button.closest('.playlist-card').querySelector('h2').innerText;
            
    console.log('Selected Text:', text);

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        const taskId = data.task_id;
        console.log("Task started. Task ID:", taskId);
        checkTaskStatus(taskId);
    })
    .catch(error => console.error("Error starting task:", error));
}

function checkTaskStatus(taskId) {
    fetch(`/status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'In Progress') {
                console.log(`Progress: ${data.progress.current}/${data.progress.total} - ${data.progress.status}`);
                setTimeout(() => checkTaskStatus(taskId), 1000);  
            } else if (data.status === 'Complete') {
                console.log("Task complete!", data.result);
                alert("Analysis complete!");
                window.location.href = `/show_results?wordcloud_path=${data.result.wordcloud_path}&six_dimensions_path=${data.result.six_dimensions_path}`;
            } else {
                console.error("Task error:", data.status);
            }
        })
        .catch(error => console.error("Error fetching task status:", error));
}

function startAnalysis(text) {
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        const taskId = data.task_id;
        console.log("Task started. Task ID:", taskId);
        checkTaskStatus(taskId);
    })
    .catch(error => console.error("Error starting task:", error));
}

function checkTaskStatus(taskId) {
    fetch(`/status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'In Progress') {
                console.log(`Progress: ${data.progress.current}/${data.progress.total} - ${data.progress.status}`);
                setTimeout(() => checkTaskStatus(taskId), 1000);  
            } else if (data.status === 'Complete') {
                console.log("Task complete!", data.result);
                alert("Analysis complete!");
                transBack(data.result)
            } else {
                console.error("Task error:", data.status);
            }
        })
        .catch(error => console.error("Error fetching task status:", error));
}


function transBack(result) {
    const data = {
        wordcloud_path: result.wordcloud_path,
        six_dimensions_path: result.six_dimensions_path
    };

    fetch('/show_results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); 
    })
    .then(html => {
        document.body.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
