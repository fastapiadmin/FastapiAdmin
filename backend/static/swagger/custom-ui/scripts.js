class LangJinDocsUI {
    constructor() {
        this.defaults = {
            url: '/openapi.json'
        }
    }
    configure(options = {}){
        // 合并用户参数和默认参数
        this.config = { ...this.defaults, ...options };
        console.log("LangJinDocsUI configured with:", this.config);
    }
    async initialize(){
        await this.buildAPIDocsData();
        this.renderUI();
    }
    async buildAPIDocsData(){
        const response = await fetch(this.config.url);
        let data = await response.json();
        this.openapi = data.openapi;
        this.info = data.info;
        this.apiData = [];
        const paths = data.paths;
        const schemas = data.components.schemas || {};
        const securitySchemes = data.components.securitySchemes || {};
        
        for (let key in paths) {
            for (let method in paths[key]) {
                this.apiData.push({
                    "operationId": paths[key][method].operationId || '',
                    "tags": paths[key][method].tags || [],
                    "summary": paths[key][method].summary || key,
                    "description": paths[key][method].description || '',
                    "path": key,
                    "method": method.toUpperCase(),
                    "headers": this.__parse_headers(paths[key][method].requestBody || {}),
                    "parameters": this.__parse_parameters(paths[key][method].parameters || []),
                    "body": this.__parse_requestBody(schemas, paths[key][method].requestBody || {}),
                    "responses": this.__parse_responses(paths[key][method].responses || {})
                });
            }
        }
        // console.log("API Documentation Data:", JSON.stringify(this.apiData));
    }
    __parse_parameters(parameters){
        let params = [];
        for (let param of parameters) {
            params.push({
                "name": param.name,
                "in": param.in,
                "required": param.required || false,
                "description": param.description || '',
                "type": param.schema.type || 'string',
                "value": "" // 添加默认空值
            });
        }
        return params;
    }
    __parse_headers(requestBody){
        if (!requestBody || Object.keys(requestBody).length === 0) {
            return {};
        }
        const content = requestBody.content || {};
        const contentTypes = Object.keys(content);
        if (contentTypes.length === 0) {
            return {};
        }
        const contentType = contentTypes[0];
        return {"Content-Type": contentType};
    }
    __parse_requestBody(schemas, requestBody){
        if (!requestBody || Object.keys(requestBody).length === 0) {
            return {};
        }
        const content = requestBody.content || {};
        const contentTypes = Object.keys(content);
        if (contentTypes.length === 0) {
            return {};
        }
        const contentType = contentTypes[0];
        const schema = content[contentType].schema;
        
        // 检查是否有 $ref 引用
        if (!schema || !schema['$ref']) {
            return {};
        }
        
        const schemaRef = schema['$ref'];
        const key = schemaRef.replace("#/components/schemas/", "");
        
        // 检查 schemas 中是否存在该 key
        if (!schemas[key]) {
            return {};
        }
        
        const properties = schemas[key].properties || {};
        const required = schemas[key].required || [];
        let body = {};
        body[contentType] = [];
        for(let key in properties){
            body[contentType].push({
                "name": key,
                "type": properties[key].type || 'string',
                "description": properties[key].description || '',
                "required": required.includes(key),
                "value": ""
            });
        }
        return body;
    }
    __parse_responses(responses){
        return {};
    }


    renderUI() {
        const container = document.getElementById('swagger-ui');
        container.innerHTML = '';

        // 创建顶部导航栏
        const navBar = document.createElement('header');
        navBar.className = 'topbar';
        navBar.innerHTML = `
            <div class="topbar-wrapper">
                <a class="logo">
                    <span>${this.info?.title || '🚀 API Documentation'}</span>
                </a>
                <div class="topbar-spacer"></div>
                <div class="topbar-actions">
                    <button class="config-button" id="configButton" title="配置全局请求头">⚙️ 配置</button>
                </div>
            </div>
        `;
        container.appendChild(navBar);

        // 创建内容布局容器
        const contentContainer = document.createElement('div');
        contentContainer.className = 'content-container';
        
        // 创建左侧菜单
        const menuContainer = document.createElement('aside');
        menuContainer.className = 'menu-container';
        menuContainer.id = 'menu-container';
        contentContainer.appendChild(menuContainer);

        // 创建主内容区
        const mainContainer = document.createElement('main');
        mainContainer.className = 'main-container';
        mainContainer.id = 'main-container';
        contentContainer.appendChild(mainContainer);

        container.appendChild(contentContainer);

        // 渲染菜单项
        this.renderMenuItems();

        // 添加搜索事件监听
        const searchInput = document.querySelector('.search-input');
        searchInput.addEventListener('input', (e) => {
            const keyword = e.target.value.trim();
            this.handleSearch(keyword);
        });

        // 添加配置按钮事件监听
        const configButton = document.getElementById('configButton');
        configButton.addEventListener('click', () => {
            this.openConfigDialog();
        });
    }

    handleSearch(keyword) {
        const menuItems = document.querySelectorAll('.menu-item');
        
        if (keyword) {
            const lowerKeyword = keyword.toLowerCase();
            
            // 遍历所有标签
            menuItems.forEach(menuItem => {
                const submenu = menuItem.nextElementSibling;
                const apiItems = submenu.querySelectorAll('.api-item');
                let hasVisibleItems = false;
                
                // 遍历当前标签下的所有API
                apiItems.forEach(apiItem => {
                    const apiPath = apiItem.dataset.path.toLowerCase();
                    const apiSummary = apiItem.querySelector('.summary').textContent.toLowerCase();
                    
                    // 检查是否匹配搜索关键词
                    if (apiPath.includes(lowerKeyword) || apiSummary.includes(lowerKeyword)) {
                        apiItem.style.display = 'block';
                        hasVisibleItems = true;
                    } else {
                        apiItem.style.display = 'none';
                    }
                });
                
                // 如果当前标签下有可见的API，则显示该标签
                if (hasVisibleItems) {
                    menuItem.style.display = 'block';
                    // 确保搜索时展开所有包含匹配项的标签
                    submenu.classList.add('show');
                    menuItem.classList.add('active');
                    menuItem.querySelector('.arrow').textContent = '▲';
                } else {
                    menuItem.style.display = 'none';
                    submenu.style.display = 'none';
                }
            });
        } else {
            // 清空搜索时恢复所有菜单项
            const menuItems = document.querySelectorAll('.menu-item');
            menuItems.forEach(menuItem => {
                menuItem.style.display = 'block';
                const submenu = menuItem.nextElementSibling;
                submenu.style.display = 'block';
            });
        }
    }

    renderMenuItems() {
        const menuContainer = document.getElementById('menu-container');
        
        // 创建搜索框
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <input class="search-input" placeholder="接口搜索..." autocomplete="off">
        `;
        menuContainer.appendChild(searchContainer);
        
        const menu = document.createElement('ul');
        menu.className = 'menu-list';
        
        // 按标签分组API
        const tagsMap = {};
        this.apiData.forEach(api => {
            api.tags.forEach(tag => {
                if (!tagsMap[tag]) {
                    tagsMap[tag] = [];
                }
                tagsMap[tag].push(api);
            });
        });

        // 创建每个标签的菜单项
        const tags = Object.keys(tagsMap);
        for (let i = 0; i < tags.length; i++) {
            const tag = tags[i];
            const count = tagsMap[tag].length;
            const menuItem = document.createElement('li');
            menuItem.className = 'menu-item';
            menuItem.innerHTML = `
                <div class="menu-item-content">
                    <span class="menu-item-title">${tag}</span>
                    <div class="menu-item-actions">
                        <span class="count">${count}</span>
                        <span class="arrow">▼</span>
                    </div>
                </div>
            `;
            menuItem.onclick = () => this.toggleMenuGroup(menuItem);
            menu.appendChild(menuItem);
            
            // 创建子菜单
            const subMenu = document.createElement('ul');
            subMenu.className = 'submenu';
            
            tagsMap[tag].forEach(api => {
                const apiItem = document.createElement('li');
                apiItem.className = 'api-item';
                apiItem.dataset.path = api.path;
                apiItem.dataset.method = api.method;
                apiItem.innerHTML = `
                    <div class="api-item-content">
                        <span class="method ${api.method.toLowerCase()}">${api.method}</span>
                        <span class="summary">${api.summary}</span>
                    </div>
                `;
                apiItem.onclick = (e) => {
                    e.stopPropagation();
                    this.showApiDetails(api);
                };
                subMenu.appendChild(apiItem);
            });
            
            menu.appendChild(subMenu);
            
            // 默认展开第一个菜单项
            if (i === 0) {
                this.toggleMenuGroup(menuItem, true);
            }
        }
        
        menuContainer.appendChild(menu);
        
        // 默认显示第一个API的详情
        if (this.apiData.length > 0) {
            this.showApiDetails(this.apiData[0]);
        }
    }

    toggleMenuGroup(menuItem, forceOpen = false) {
        const submenu = menuItem.nextElementSibling;
        const arrow = menuItem.querySelector('.arrow');
        
        if (submenu.classList.contains('show') && !forceOpen) {
            // 折叠菜单
            submenu.classList.remove('show');
            menuItem.classList.remove('active');
            arrow.textContent = '▼';
        } else {
            // 展开菜单
            submenu.classList.add('show');
            menuItem.classList.add('active');
            arrow.textContent = '▲';
        }
    }

    showApiDetails(api) {
        const mainContainer = document.getElementById('main-container');
        
        // 保存当前选中的API
        this.currentApi = api;
        
        // 高亮当前选中的菜单项
        document.querySelectorAll('.api-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`.api-item[data-path="${api.path}"][data-method="${api.method}"]`).classList.add('active');
        
        // 渲染API详情
        mainContainer.innerHTML = `
            <div class="api-details">
                <div class="api-header">
                    <h1 class="api-title">${api.summary}</h1>
                    <p class="api-description">${api.description || ''}</p>
                    <div class="api-meta">
                        <select class="method-select" id="method-select">
                            <option value="GET" ${api.method === 'GET' ? 'selected' : ''}>GET</option>
                            <option value="POST" ${api.method === 'POST' ? 'selected' : ''}>POST</option>
                            <option value="PUT" ${api.method === 'PUT' ? 'selected' : ''}>PUT</option>
                            <option value="DELETE" ${api.method === 'DELETE' ? 'selected' : ''}>DELETE</option>
                            <option value="PATCH" ${api.method === 'PATCH' ? 'selected' : ''}>PATCH</option>
                        </select>
                        <input type="text" class="path-input" id="path-input" value="${api.path}">
                        <button class="send-button" onclick="ui.sendRequest()">Send</button>
                    </div>
                </div>
                
                <!-- 请求参数区域 -->
                <div class="section-container">
                    <h2 class="section-title">请求参数</h2>
                    <div class="request-tabs tabs">
                        <button class="tab active" data-tab="parameters">Parameters</button>
                        <button class="tab" data-tab="headers">Headers</button>
                        <button class="tab" data-tab="requestBody">Body</button>
                    </div>
                    
                    <div class="request-tab-content tab-content">
                        <div class="tab-pane active" id="parameters">
                            ${this.renderParametersTab(api.parameters)}
                        </div>
                        <div class="tab-pane" id="headers">
                            ${this.renderHeadersTab(api.headers)}
                        </div>
                        <div class="tab-pane" id="requestBody">
                            ${this.renderRequestBodyTab(api.body)}
                        </div>
                    </div>
                </div>
                
                <!-- 响应实例区域 -->
                <div class="section-container">
                    <h2 class="section-title">响应实例</h2>
                    <div class="response-section">
                        ${this.renderResponseSection(api)}
                    </div>
                </div>
            </div>
        `;
        
        // 添加标签切换事件
        document.querySelectorAll('.request-tabs .tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.request-tabs .tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.request-tab-content .tab-pane').forEach(p => p.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tab.dataset.tab).classList.add('active');
            });
        });
    }

    renderParametersTab(parameters) {
        let hasParams = parameters && parameters.length > 0;
        
        return `
            <div class="params-section">
                <table class="params-table">
                    <thead>
                        <tr>
                            <th>参数名</th>
                            <th>值</th>
                            <th>类型</th>
                            <th>是否必填</th>
                            <th>简述</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="parameters-table-body">
                        ${hasParams ? parameters.map((param, index) => `
                        <tr>
                            <td><input type="text" class="editable-input" value="${param.name}" placeholder="参数名"></td>
                            <td><input type="text" class="editable-input" value="${param.value}" placeholder="值"></td>
                            <td>
                                <select class="editable-input">
                                    <option value="string" ${param.type === 'string' ? 'selected' : ''}>string</option>
                                    <option value="number" ${param.type === 'number' ? 'selected' : ''}>number</option>
                                    <option value="boolean" ${param.type === 'boolean' ? 'selected' : ''}>boolean</option>
                                    <option value="array" ${param.type === 'array' ? 'selected' : ''}>array</option>
                                    <option value="object" ${param.type === 'object' ? 'selected' : ''}>object</option>
                                </select>
                            </td>
                            <td>
                                <div class="checkbox-container">
                                    <input type="checkbox" ${param.required ? 'checked' : ''}>
                                </div>
                            </td>
                            <td><input type="text" class="editable-input" value="${param.description}" placeholder="简述"></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-delete" onclick="ui.deleteParameterRow(this)">删除</button>
                                </div>
                            </td>
                        </tr>
                        `).join('') : `
                        <tr>
                            <td><input type="text" class="editable-input" placeholder="参数名"></td>
                            <td><input type="text" class="editable-input" placeholder="值"></td>
                            <td>
                                <select class="editable-input">
                                    <option value="string">string</option>
                                    <option value="number">number</option>
                                    <option value="boolean">boolean</option>
                                    <option value="array">array</option>
                                    <option value="object">object</option>
                                </select>
                            </td>
                            <td>
                                <div class="checkbox-container">
                                    <input type="checkbox">
                                </div>
                            </td>
                            <td><input type="text" class="editable-input" placeholder="简述"></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-delete" onclick="ui.deleteParameterRow(this)">删除</button>
                                </div>
                            </td>
                        </tr>
                        `}
                    </tbody>
                </table>
                <div class="table-actions">
                    <button class="btn btn-add" onclick="ui.addParameterRow()">新增参数</button>
                </div>
            </div>
        `;
    }

    renderHeadersTab(headers) {
        let hasHeaders = headers && Object.keys(headers).length > 0;
        
        return `
            <div class="params-section">
                <table class="params-table">
                    <thead>
                        <tr>
                            <th>参数名</th>
                            <th>值</th>
                            <th>是否必填</th>
                            <th>简述</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="headers-table-body">
                        ${hasHeaders ? Object.entries(headers).map(([key, value], index) => `
                        <tr>
                            <td><input type="text" class="editable-input" value="${key}" placeholder="参数名"></td>
                            <td><input type="text" class="editable-input" value="${value}" placeholder="值"></td>
                            <td>
                                <div class="checkbox-container">
                                    <input type="checkbox" checked>
                                </div>
                            </td>
                            <td><input type="text" class="editable-input" placeholder="简述"></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-delete" onclick="ui.deleteHeaderRow(this)">删除</button>
                                </div>
                            </td>
                        </tr>
                        `).join('') : `
                        <tr>
                            <td><input type="text" class="editable-input" placeholder="参数名"></td>
                            <td><input type="text" class="editable-input" placeholder="值"></td>
                            <td>
                                <div class="checkbox-container">
                                    <input type="checkbox">
                                </div>
                            </td>
                            <td><input type="text" class="editable-input" placeholder="简述"></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-delete" onclick="ui.deleteHeaderRow(this)">删除</button>
                                </div>
                            </td>
                        </tr>
                        `}
                    </tbody>
                </table>
                <div class="table-actions">
                    <button class="btn btn-add" onclick="ui.addHeaderRow()">新增头部</button>
                </div>
            </div>
        `;
    }

    renderRequestBodyTab(body) {
        // 默认显示 JSON 编辑器，即使没有 body 参数
        const contentType = Object.keys(body)[0] || 'application/json';
        const params = body[contentType] || [];

        if (contentType.includes('application/json')) {
            // JSON格式的请求体
            const jsonValue = params.length > 0 ? JSON.stringify(this.__createRequestBodyJSON(params), null, 2) : '{}';
            return `
                <div class="json-editor-container">
                    <textarea class="json-editor" placeholder="示例: {&quot;key&quot;: &quot;value&quot;} 请使用双引号&quot; 而不是单引号">${jsonValue}</textarea>
                </div>
            `;
        } else {
            // 表单格式的请求体
            return `
                <div class="params-section">
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>值</th>
                                <th>类型</th>
                                <th>是否必填</th>
                                <th>简述</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="body-table-body">
                            ${params.length > 0 ? params.map((param, index) => `
                            <tr>
                                <td><input type="text" class="editable-input" value="${param.name}" placeholder="参数名"></td>
                                <td><input type="text" class="editable-input" value="${param.value}" placeholder="值"></td>
                                <td>
                                    <select class="editable-input">
                                        <option value="string" ${param.type === 'string' ? 'selected' : ''}>string</option>
                                        <option value="number" ${param.type === 'number' ? 'selected' : ''}>number</option>
                                        <option value="boolean" ${param.type === 'boolean' ? 'selected' : ''}>boolean</option>
                                        <option value="array" ${param.type === 'array' ? 'selected' : ''}>array</option>
                                        <option value="object" ${param.type === 'object' ? 'selected' : ''}>object</option>
                                    </select>
                                </td>
                                <td>
                                    <div class="checkbox-container">
                                        <input type="checkbox" ${param.required ? 'checked' : ''}>
                                    </div>
                                </td>
                                <td><input type="text" class="editable-input" value="${param.description}" placeholder="简述"></td>
                                <td>
                                    <div class="action-buttons">
                                        <button class="btn btn-delete" onclick="ui.deleteBodyRow(this)">删除</button>
                                    </div>
                                </td>
                            </tr>
                            `).join('') : ''}
                        </tbody>
                    </table>
                    <div class="table-actions">
                        <button class="btn btn-add" onclick="ui.addBodyRow()">新增参数</button>
                    </div>
                </div>
            `;
        }
    }

    __createRequestBodyJSON(params) {
        const json = {};
        params.forEach(param => {
            let value = param.value;
            if (param.type === 'number') {
                value = value ? Number(value) : 0;
            } else if (param.type === 'boolean') {
                value = value.toLowerCase() === 'true' || value === '1';
            } else if (param.type === 'array') {
                value = value ? value.split(',').map(item => item.trim()) : [];
            } else if (param.type === 'object') {
                try {
                    value = JSON.parse(value);
                } catch (e) {
                    value = {};
                }
            }
            json[param.name] = value;
        });
        return json;
    }

    renderResponseSection(api) {
        return `
            <div class="response-container">
                <div class="response-body">
                    <pre><code class="json">{}</code></pre>
                </div>
            </div>
        `;
    }

    sendRequest() {
        const method = document.getElementById('method-select').value;
        const path = document.getElementById('path-input').value;

        // 显示加载状态
        const responseContainer = document.querySelector('.response-body pre code');
        responseContainer.textContent = 'Loading...';

        // 获取参数
        const params = this.__getParametersFromForm();
        const headers = this.__getHeadersFromForm();
        const body = this.__getBodyFromForm();

        // 获取全局配置的请求头
        const globalHeaders = this.__getGlobalHeaders();

        // 合并请求头（全局配置优先）
        const mergedHeaders = { ...globalHeaders, ...headers };

        // 构建请求URL
        let url = path;
        if (Object.keys(params).length > 0) {
            url += '?' + new URLSearchParams(params).toString();
        }

        // 构建请求选项
        const options = {
            method: method,
            headers: mergedHeaders
        };

        // 添加请求体（如果有）
        if (Object.keys(body).length > 0) {
            options.body = JSON.stringify(body);
        }

        // 发送请求
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                // 显示响应
                responseContainer.textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                // 显示错误
                responseContainer.textContent = 'Error: ' + error.message;
            });
    }

    __getParametersFromForm() {
        const params = {};
        const rows = document.querySelectorAll('#parameters-table-body tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const name = cells[0].querySelector('input').value;
            const value = cells[1].querySelector('input').value;
            const required = cells[3].querySelector('input').checked;
            
            if (name && (value || required)) {
                params[name] = value;
            }
        });
        
        return params;
    }

    __getHeadersFromForm() {
        const headers = {};
        const rows = document.querySelectorAll('#headers-table-body tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const name = cells[0].querySelector('input').value;
            const value = cells[1].querySelector('input').value;
            const required = cells[2].querySelector('input').checked;
            
            if (name && (value || required)) {
                headers[name] = value;
            }
        });
        
        return headers;
    }

    __getBodyFromForm() {
        if (!this.currentApi) {
            return {};
        }

        const contentType = Object.keys(this.currentApi.body)[0] || 'application/json';

        if (contentType.includes('application/json')) {
            // 从JSON编辑器获取请求体
            const jsonEditor = document.querySelector('.json-editor');
            if (!jsonEditor) {
                return {};
            }
            let value = jsonEditor.value.trim();
            if (!value) {
                return {};
            }
            return this.robustJsonParse(value);
        } else {
            // 从表单获取请求体
            const body = {};
            const rows = document.querySelectorAll('#body-table-body tr');

            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const name = cells[0].querySelector('input').value;
                const value = cells[1].querySelector('input').value;
                const required = cells[3].querySelector('input').checked;

                if (name && (value || required)) {
                    body[name] = value;
                }
            });

            return body;
        }
    }

    addParameterRow() {
        const tableBody = document.getElementById('parameters-table-body');
        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `
            <td><input type="text" class="editable-input" placeholder="参数名"></td>
            <td><input type="text" class="editable-input" placeholder="值"></td>
            <td>
                <select class="editable-input">
                    <option value="string">string</option>
                    <option value="number">number</option>
                    <option value="boolean">boolean</option>
                    <option value="array">array</option>
                    <option value="object">object</option>
                </select>
            </td>
            <td>
                <div class="checkbox-container">
                    <input type="checkbox">
                </div>
            </td>
            <td><input type="text" class="editable-input" placeholder="简述"></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-delete" onclick="ui.deleteParameterRow(this)">删除</button>
                </div>
            </td>
        `;
        
        tableBody.appendChild(newRow);
    }

    deleteParameterRow(button) {
        const row = button.closest('tr');
        row.remove();
    }

    addHeaderRow() {
        const tableBody = document.getElementById('headers-table-body');
        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `
            <td><input type="text" class="editable-input" placeholder="参数名"></td>
            <td><input type="text" class="editable-input" placeholder="值"></td>
            <td>
                <div class="checkbox-container">
                    <input type="checkbox">
                </div>
            </td>
            <td><input type="text" class="editable-input" placeholder="简述"></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-delete" onclick="ui.deleteHeaderRow(this)">删除</button>
                </div>
            </td>
        `;
        
        tableBody.appendChild(newRow);
    }

    deleteHeaderRow(button) {
        const row = button.closest('tr');
        row.remove();
    }

    addBodyRow() {
        const tableBody = document.getElementById('body-table-body');
        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `
            <td><input type="text" class="editable-input" placeholder="参数名"></td>
            <td><input type="text" class="editable-input" placeholder="值"></td>
            <td>
                <select class="editable-input">
                    <option value="string">string</option>
                    <option value="number">number</option>
                    <option value="boolean">boolean</option>
                    <option value="array">array</option>
                    <option value="object">object</option>
                </select>
            </td>
            <td>
                <div class="checkbox-container">
                    <input type="checkbox">
                </div>
            </td>
            <td><input type="text" class="editable-input" placeholder="简述"></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-delete" onclick="ui.deleteBodyRow(this)">删除</button>
                </div>
            </td>
        `;
        
        tableBody.appendChild(newRow);
    }

    deleteBodyRow(button) {
        const row = button.closest('tr');
        row.remove();
    }

    // 打开配置对话框
    openConfigDialog() {
        const globalHeaders = this.__getGlobalHeaders();
        const configDialog = document.createElement('div');
        configDialog.className = 'config-dialog-overlay';
        configDialog.innerHTML = `
            <div class="config-dialog">
                <div class="config-dialog-header">
                    <h3>配置全局请求头</h3>
                    <button class="close-button" id="closeConfigDialog">×</button>
                </div>
                <div class="config-dialog-body">
                    <table class="config-table">
                        <thead>
                            <tr>
                                <th>Key</th>
                                <th>Value</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="configTableBody">
                            ${Object.entries(globalHeaders).map(([key, value]) => `
                                <tr>
                                    <td><input type="text" class="config-input" value="${key}" placeholder="Header Key"></td>
                                    <td><input type="text" class="config-input" value="${value}" placeholder="Header Value"></td>
                                    <td><button class="btn btn-delete" onclick="ui.deleteConfigRow(this)">删除</button></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                    <div class="table-actions">
                        <button class="btn btn-add" onclick="ui.addConfigRow()">新增</button>
                    </div>
                </div>
                <div class="config-dialog-footer">
                    <button class="btn btn-primary" onclick="ui.saveConfig()">保存</button>
                    <button class="btn" onclick="ui.closeConfigDialog()">取消</button>
                </div>
            </div>
        `;
        document.body.appendChild(configDialog);

        // 绑定关闭事件
        document.getElementById('closeConfigDialog').addEventListener('click', () => this.closeConfigDialog());
        configDialog.addEventListener('click', (e) => {
            if (e.target === configDialog) {
                this.closeConfigDialog();
            }
        });
    }

    // 关闭配置对话框
    closeConfigDialog() {
        const dialog = document.querySelector('.config-dialog-overlay');
        if (dialog) {
            dialog.remove();
        }
    }

    // 添加配置行
    addConfigRow() {
        const tableBody = document.getElementById('configTableBody');
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="config-input" placeholder="Header Key"></td>
            <td><input type="text" class="config-input" placeholder="Header Value"></td>
            <td><button class="btn btn-delete" onclick="ui.deleteConfigRow(this)">删除</button></td>
        `;
        tableBody.appendChild(newRow);
    }

    // 删除配置行
    deleteConfigRow(button) {
        const row = button.closest('tr');
        row.remove();
    }

    // 保存配置
    saveConfig() {
        const rows = document.querySelectorAll('#configTableBody tr');
        const headers = {};

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const key = cells[0].querySelector('input').value.trim();
            const value = cells[1].querySelector('input').value.trim();

            if (key && value) {
                headers[key] = value;
            }
        });

        // 保存到本地存储
        localStorage.setItem('globalHeaders', JSON.stringify(headers));

        // 显示成功提示
        this.showNotification('配置已保存');

        // 关闭对话框
        this.closeConfigDialog();
    }

    // 从本地存储获取全局请求头
    __getGlobalHeaders() {
        const stored = localStorage.getItem('globalHeaders');
        if (stored) {
            try {
                return JSON.parse(stored);
            } catch (e) {
                return {};
            }
        }
        return {};
    }

    // 显示通知
    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // 增强版JSON解析，处理非标准JSON格式
    robustJsonParse(str) {
        if (!str || !str.trim()) return {};
        const trimmed = str.trim();
        try {
            return JSON.parse(trimmed);
        } catch (e) {
            console.log('标准JSON解析失败，尝试修复:', trimmed);
            try {
                let processed = trimmed;
                // 1. 处理用单引号包裹整个对象的情况 (您原有的逻辑，很好)
                if (processed.startsWith("'") && processed.endsWith("'")) {
                    processed = processed.slice(1, -1);
                }
                // 2. 【核心改进】智能替换键名
                // 匹配 'key': 或 "key": 或 key: 的模式，统一替换为 "key":
                // (\w+) 捕获键名 (字母、数字、下划线)
                processed = processed.replace(/['"]?(\w+)['"]?\s*:/g, '"$1":');
                // 3. 【核心改进】智能替换字符串值
                // 匹配 : '...' 的模式，只替换值的单引号为双引号
                // 这样可以确保不会影响到字符串内部的合法单引号
                // ([^']*) 捕获不包含单引号的任意字符序列
                processed = processed.replace(/:\s*'([^']*)'/g, ':"$1"');
                // 4. (可选) 处理布尔值和null的小写问题 (如果后端返回的是大写 TRUE/FALSE)
                // processed = processed.replace(/\bTRUE\b/g, 'true');
                // processed = processed.replace(/\bFALSE\b/g, 'false');
                // processed = processed.replace(/\bNULL\b/g, 'null');
                // 5. (可选) 清理可能因替换产生的多余逗号，例如 [1,2,,] -> [1,2]
                // processed = processed.replace(/,\s*,/g, ',').replace(/,\s*]/g, ']').replace(/,\s*}/g, '}');
                console.log('修复后的JSON字符串:', processed);
                // 6. 尝试解析修复后的字符串
                const result = JSON.parse(processed);
                console.log('修复后的JSON对象:', result);
                return result;
            } catch (e2) {
                // 【您原有的错误处理逻辑，保持不变】
                console.error('JSON解析最终失败:', e2);
                console.error('失败的处理结果:', processed);
                this.showNotification('JSON 格式错误，请检查引号和语法');
                return {};
            }
        }
    }
    
}

const ui = new LangJinDocsUI();