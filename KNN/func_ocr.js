//客户端逻辑
//func_ocr.js
var func_ocr = {
    Canvas_w: 320,
    Translate_w: 32,
    Pixel_w: 10, 
    Batch_s: 1,

    // 服务器端参数
    PORT_NUMBER:"9000",
    HOST_NAME:"http://localhost",

    // 颜色变量
    White: "#000000",
    Black: "#ffffff",

    // 客户端训练数据集
    
    trainArray: [],
    trainingRequestCount: 0,

    onLoadFunction: function() {
        this.resetCanvas();
    },
    //重置逻辑功能实现
    resetCanvas: function() {
        var canvas = document.getElementById('canvas');
        var tmp = canvas.getContext('2d');

        this.data = [];
        tmp.fillStyle = this.White;
        tmp.fillRect(0, 0, this.Canvas_w, this.Canvas_w);
        var matrixSize = 1024;
        while (matrixSize--) this.data.push(0);
        this.drawGrid(tmp);

        canvas.onmousemove = function(e) { this.onMouseMove(e, tmp, canvas) }.bind(this);
        canvas.onmousedown = function(e) { this.onMouseDown(e, tmp, canvas) }.bind(this);
        canvas.onmouseup = function(e) { this.onMouseUp(e, tmp) }.bind(this);
    },

    drawGrid: function(tmp) {
        for (var x = this.Pixel_w, y = this.Pixel_w; x < this.Canvas_w; x += this.Pixel_w, y += this.Pixel_w) {
            tmp.strokeStyle = this.Black;
            tmp.beginPath();
            tmp.moveTo(x, 0);
            tmp.lineTo(x, this.Canvas_w);
            tmp.stroke();

            tmp.beginPath();
            tmp.moveTo(0, y);
            tmp.lineTo(this.Canvas_w, y);
            tmp.stroke();
        }
    },

    onMouseMove: function(e, tmp, canvas) {
        if (!canvas.isDrawing) {
            return;
        }
        this.fillSquare(tmp, e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        //this.fillSquare(tmp, e.clientY - canvas.offsetTop, e.clientX - canvas.offsetLeft);

    },

    onMouseDown: function(e, tmp, canvas) {
        canvas.isDrawing = true;
        this.fillSquare(tmp, e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        //this.fillSquare(tmp, e.clientY - canvas.offsetTop, e.clientX - canvas.offsetLeft);

    },

    onMouseUp: function(e) {
        canvas.isDrawing = false;
    },

    fillSquare: function(tmp, x, y) {
        var xPixel = Math.floor(x / this.Pixel_w);
        var yPixel = Math.floor(y / this.Pixel_w);
        // 存储手写输入数据
        this.data[((yPixel - 1)*this.Translate_w   + xPixel) - 1] = 1;
        //this.data[((xPixel - 1)  * this.Translate_w + yPixel) - 1] = 1;
        tmp.fillStyle = '#ffffff';
        tmp.fillRect(xPixel * this.Pixel_w, yPixel * this.Pixel_w, this.Pixel_w, this.Pixel_w);
    },

    train: function() {
        var digitVal = document.getElementById("digit").value;
        if (!digitVal || this.data.indexOf(1) < 0) {
            alert("输入一个数字用于训练...");
            return;
        }
        // 将数据加入客户端训练数据集
        this.trainArray.push({"y0": this.data, "label": parseInt(digitVal)});
        this.trainingRequestCount++;
        // 将客服端训练数据集发送给服务器端
        if (this.trainingRequestCount == this.Batch_s) {
            alert("发送训练数据至服务器...");
            var json = {
                trainArray: this.trainArray,
                train: true
            };
            this.sendData(json);
            this.trainingRequestCount = 0;
            this.trainArray = [];
        }
        alert("数据传输完成");
    },

    // 发送预测请求
    test: function() {
        if (this.data.indexOf(1) < 0) {
            alert("输入一个数字用于神经网络测试...");
            return;
        }
        //alert(this.data);
        var json = {
            image: this.data,
            predict: true
        };
        this.sendData(json);
    },

    // 处理服务器响应
    receiveResponse: function(xmlHttp) {
        if (xmlHttp.status != 200) {
            alert("服务器返回状态为： " + xmlHttp.status);
            return;
        }
        var responseJSON = JSON.parse(xmlHttp.responseText);
        if (xmlHttp.responseText && responseJSON.type == "test") {
            alert("神经网络的预测值为：\'" + responseJSON.result + '\'');
        }
    },

    onError: function(e) {
        alert("连接服务器产生的错误： " + e.target.statusText);
    },

    sendData: function(json) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open('POST', this.HOST_NAME + ":" + this.PORT_NUMBER, false);
        xmlHttp.onload = function() { this.receiveResponse(xmlHttp); }.bind(this);
        xmlHttp.onerror = function() { this.onError(xmlHttp) }.bind(this);
        var msg = JSON.stringify(json);
        xmlHttp.setRequestHeader('Content-length', msg.length);
        xmlHttp.setRequestHeader("Connection", "close");
        xmlHttp.send(msg);
    }
}

