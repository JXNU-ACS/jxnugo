var uploaderoption = {
    runtimes: 'html5,flash,html4', // 上传模式,依次退化
    browse_button: 'pickfiles', // 上传选择的点选按钮，**必需**
    // 在初始化时，uptoken, uptoken_url, uptoken_func 三个参数中必须有一个被设置
    // 切如果提供了多个，其优先级为 uptoken > uptoken_url > uptoken_func
    // 其中 uptoken 是直接提供上传凭证，uptoken_url 是提供了获取上传凭证的地址，如果需要定制获取 uptoken 的过程则可以设置 uptoken_func
    //uptoken : "BK58FryE-_YddhrnjmpS_phqj3vKrR3k-svdydGB:g-wo-Jf46gBQq2mZuoVUvlKcpJM=:eyJzY29wZSI6InRyYWRlOlVVSUQoJzk5Mzg5MWIyLTFkMmUtNDcxZi1hMjBkLWZiM2U0NzM0ZWQ4ZScpIiwiZGVhZGxpbmUiOjE0NjI4MTA2Mzl9", // uptoken 是上传凭证，由其他程序生成
    //uptoken: "BK58FryE-_YddhrnjmpS_phqj3vKrR3k-svdydGB:_s873eUIuGT_OqdJy1H3S2ZgP0Y=:eyJzY29wZSI6InRyYWRlIiwiZGVhZGxpbmUiOjE0NjI4MDY2MTZ9",
    uptoken_url: $('#uptoken_url').val(), // Ajax 请求 uptoken 的 Url，**强烈建议设置**（服务端提供）
    // uptoken_func: function(file){    // 在需要获取 uptoken 时，该方法会被调用
    //    // do something
    //    return uptoken;
    // },
    get_new_uptoken: true, // 设置上传文件的时候是否每次都重新获取新的 uptoken
    // downtoken_url: '/downtoken',
    // Ajax请求downToken的Url，私有空间时使用,JS-SDK 将向该地址POST文件的key和domain,服务端返回的JSON必须包含`url`字段，`url`值为该文件的下载地址
    //unique_names: true,              // 默认 false，key 为文件名。若开启该选项，JS-SDK 会为每个文件自动生成key（文件名）
    //save_key: true, // 默认 false。若在服务端生成 uptoken 的上传策略中指定了 `sava_key`，则开启，SDK在前端将不对key进行任何处理
    domain: $('#domain').val(), // bucket 域名，下载资源时用到，**必需**
    container: 'upload-aira', // 上传区域 DOM ID，默认是 browser_button 的父元素，
    max_file_size: '10mb', // 最大文件体积限制
    flash_swf_url: "static/js/plupload/Moxie.swf", //'path/of/plupload/Moxie.swf',  //引入 flash,相对路径
    max_retries: 3, // 上传失败最大重试次数
    dragdrop: true, // 开启可拖曳上传
    drop_element: 'upload-aira', // 拖曳上传区域元素的 ID，拖曳文件或文件夹后可触发上传
    chunk_size: '1024kb', // 分块上传时，每块的体积
    auto_start: true, // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,

    multi_selection: false, // 设置一次只能选择一个文件
    //x_vars : {
    //    自定义变量，参考http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html
    //    'time' : function(up,file) {
    //        var time = (new Date()).getTime();
    // do something with 'time'
    //        return time;
    //    },
    //    'size' : function(up,file) {
    //        var size = file.size;
    // do something with 'size'
    //        return size;
    //    }
    //},
    filters: {
        mime_types: [
            { title: "Image files", extensions: "jpg,gif,png" }
        ]
    },
    init: {
        'FilesAdded': function(up, files) {
            plupload.each(files, function(file) {
                // 文件添加进队列后,处理相关的事情
                var ui = new FileuploadUI(file);
                ui.crateImg();
                ui.imgStatus(0,"等待上传");
                ui.bindUploadCancel(up);
            });
        },
        'BeforeUpload': function(up, file) {
            // 每个文件上传前,处理相关的事情

        },
        'UploadProgress': function(up, file) {
            // 每个文件上传时,处理相关的事情
            var ui = new FileuploadUI(file);
                
                ui.imgStatus(1);
        },
        'FileUploaded': function(up, file, info) {
            // 每个文件上传成功后,处理相关的事情
            // 其中 info 是文件上传成功后，服务端返回的json，形式如
            // {
            //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
            //    "key": "gogopher.jpg"
            //  }
            // 参考http://developer.qiniu.com/docs/v6/api/overview/up/response/simple-response.html

            var domain = up.getOption('domain');
            var res = jQuery.parseJSON(info);
            var sourceLink = "http://"+domain +"/"+res.key; //获取上传成功后的文件的Url
            var simgLink = Qiniu.watermark(postimg,res.key);
            var ui = new FileuploadUI(file);
            ui.eachUpload(simgLink,res.key);
            ui.bindUploadCancel(up);
            ui.getJson();
        },
        'Error': function(up, err, errTip) {
            //上传出错时,处理相关的事情
            var ui = new FileuploadUI(file);
            ui.imgStatus(0,"上传失败");
        },
        'UploadComplete': function() {
            //队列文件处理完毕后,处理相关的事情
        },
        //'Key': function(up, file) {
        // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
        // 该配置必须要在 unique_names: false , save_key: false 时才生效

        //var key = "";
        // do something with key here
        //return key
        //}
    }

};

var userimgupload = {
    runtimes: 'html5,flash,html4', // 上传模式,依次退化
    browse_button: 'pickfiles',
    uptoken_url: $('#uptoken_url').val(),
    get_new_uptoken: true,
    domain: $('#domain').val(),
    container: 'upload-aira',
    max_file_size: '10mb',
    flash_swf_url: "static/js/plupload/Moxie.swf", 
    max_retries: 3,
    dragdrop: true,
    drop_element: 'upload-aira',
    chunk_size: '1024kb',
    auto_start: true,
    multi_selection: false,
    filters: {
        mime_types: [
            { title: "Image files", extensions: "jpg,gif,png" }
        ]
    },
    init: {
        'FilesAdded': function(up, files) {
            plupload.each(files, function(file) {
                // 文件添加进队列后,处理相关的事情
                var ui = new UserImgUpload(file);
                
                ui.imgStatus(0,"等待..");
            });
        },
        'BeforeUpload': function(up, file) {
            // 每个文件上传前,处理相关的事情

        },
        'UploadProgress': function(up, file) {
            // 每个文件上传时,处理相关的事情
            var ui = new UserImgUpload(file);
                
                ui.imgStatus(1);
        },
        'FileUploaded': function(up, file, info) {
            var domain = up.getOption('domain');
            var res = jQuery.parseJSON(info);
            var sourceLink = "http://"+domain +"/"+res.key; //获取上传成功后的文件的Url

            var ui = new UserImgUpload(file);
            ui.imgStatus(0,"上传头像");
            ui.setImg(sourceLink);
        },
        'Error': function(up, err, errTip) {
            var ui = new UserImgUpload(file);
            //上传出错时,处理相关的事情
            ui.imgStatus(0,"上传失败");
        },
        'UploadComplete': function() {
            //队列文件处理完毕后,处理相关的事情
            var ui = new UserImgUpload(file);
            ui.imgStatus(0,"上传头像");
        },
    },
};
var usrimg = {
     mode: 3,  // 缩略模式，共6种[0-5]
       w: 300,   // 具体含义由缩略模式决定
       h: 200,   // 具体含义由缩略模式决定
       q: 100,   // 新图的图像质量，取值范围：1-100
       format: 'jpg'  // 新图的输出格式，取值范围：jpg，gif，png，webp等
};
var postimg = {
    mode: 3,  // 缩略模式，共6种[0-5]
       w: 800,   // 具体含义由缩略模式决定
       h: 600,   // 具体含义由缩略模式决定
       q: 100,   // 新图的图像质量，取值范围：1-100
       format: 'jpg'
};