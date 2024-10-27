// readjson.js
window.addEventListener('pywebviewready', function() {
    // DOM 内容完全加载后执行 fetchJsonFiles 函数
    fetchJsonFiles();
});

function fetchJsonFiles() {
    // 直接调用 pywebview.api.list_json_files 而不是 pywebview.api('list_json_files', {})
    pywebview.api.list_json_files()
        .then(jsonFiles => {
            updateSelect(jsonFiles);
        })
        .catch(error => {
            console.error('There was a problem with fetching the JSON files:', error);
        });
}

function fetchJsonData(fileName) {
    // 确保传递给 get_json_data 的是文件名字符串，而不是包含该字符串的字典
    pywebview.api.get_json_data(fileName)
        .then(data => {
            updatePage(data);
        })
        .catch(error => {
            console.error('There was a problem with fetching the JSON data:', error);
        });
}

function updateSelect(jsonFiles) {
    const select = document.getElementById('jsonSelect');
    select.innerHTML = ''; // 清空现有选项
    const defaultOption = document.createElement('option');
    defaultOption.value = ''; // 通常提示选项的 value 为空
    defaultOption.textContent = '--请先选择json文件哦awa--';
    defaultOption.disabled = true; // 可选：使提示选项不可选
    defaultOption.selected = true; // 设置提示选项为默认选中
    select.appendChild(defaultOption);
    jsonFiles.forEach(file => {
        const option = document.createElement('option');
        option.value = file;
        option.textContent = file;
        select.appendChild(option);
    });
    select.addEventListener('change', function() {
        const selectedFile = select.value;
        if (selectedFile) {
            fetchJsonData(selectedFile);
        }
    });
}

function updatePage(data) {
    const container = document.getElementById('jsonContainer');
    container.innerHTML = ''; // 清空现有内容

    // 处理主信息
    const mainInfo = data;
    const mainContent = `
        <div class="main-info">
            <img src="${mainInfo.logo}" alt="Logo" style="width:100px;height:auto;">
            <h1>${mainInfo.title}</h1>
            <p>${mainInfo.describe}</p>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', mainContent);

    // 处理其他项目
    mainInfo.items.forEach(item => {
        // 根据 item.type 的值来决定是否给 a 标签添加 target="_blank" 属性
        const targetBlank = item.type == 0 ? ' target="_blank"' : '';
        const content = `
            <div class="grid-item">
                <h3>${item.title}</h3>
                <!-- 根据 type 类型决定是否添加 target 属性 -->
                <a href="${item.src}"${targetBlank}>点击查看</a>
                <!-- 确保 item.imgsrc 存在且有有效值，才创建 img 标签 -->
                ${item.imgsrc ? `<img src="${item.imgsrc}" alt="Image" style="width:100px;height:auto;">` : ''}
                <p>${item.describe}</p>
            </div>
        `;

        // 将创建的内容添加到容器中
        container.insertAdjacentHTML('beforeend', content);
    });
}
