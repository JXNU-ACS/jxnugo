var uploaderoption = {
    runtimes: 'html5,flash,html4', 
    browse_button: 'pickfiles', 
    uptoken_url: "/get_upload_token", 
    get_new_uptoken: true, 
    
    unique_names: true,             
    save_key: true, 
    domain: "7xrkww.com1.z0.glb.clouddn.com", 
    container: 'upload-aira', 
    max_file_size: '10mb', 
    flash_swf_url: "static/js/plupload/Moxie.swf", 
    max_retries: 3, 
    dragdrop: true, 
    drop_element: 'upload-aira', 
    chunk_size: '10mb', 
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
                
                var ui = new FileuploadUI(file);
                ui.crateImg();
                ui.imgStatus(0,"等待上传");
                ui.bindUploadCancel(up);
            });
        },
        'BeforeUpload': function(up, file) {
        },
        'UploadProgress': function(up, file) {
            var ui = new FileuploadUI(file);
                
                ui.imgStatus(1);
        },
        'FileUploaded': function(up, file, info) {
           

            var domain = up.getOption('domain');
            var res = jQuery.parseJSON(info);
            var sourceLink = "http://"+domain +"/"+res.key; //获取上传成功后的文件的Url
            var simgLink = "http://"+Qiniu.imageView2(postimg,res.key);
            var ui = new FileuploadUI(file);
            ui.eachUpload(simgLink,res.key);
            ui.bindUploadCancel(up);
            ui.getJson(res.key);
        },
        'Error': function(up, err, errTip) {
            var ui = new FileuploadUI();
            ui.imgStatus(0,"上传失败");
        },
        'UploadComplete': function() {
            
        },
    }

};

var userimgupload = {
    runtimes: 'html5,flash,html4', // 上传模式,依次退化
    browse_button: 'pickfiles',
    uptoken_url: "/get_upload_token",
    get_new_uptoken: true,
    domain: "7xrkww.com1.z0.glb.clouddn.com",
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
                
                ui.imgStatus(0,"等待上传");
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
            var simgLink = "http://"+Qiniu.imageView2(usrimg,res.key);
            var ui = new UserImgUpload(file);
            ui.imgStatus(0,"上传头像");
            ui.setImg(simgLink);
            
        },
        'Error': function(up, err, errTip) {
            var ui = new UserImgUpload(file);
            //上传出错时,处理相关的事情
            ui.imgStatus(0,"上传失败");
        },
        'UploadComplete': function() {
            //队列文件处理完毕后,处理相关的事情
            var ui = new UserImgUpload();
            ui.imgStatus(0,"上传头像");
        },
    },
};
var usrimg = {
     mode: 3,  // 缩略模式，共6种[0-5]
       w: 300,   // 具体含义由缩略模式决定
       //h: 200,   // 具体含义由缩略模式决定
       q: 100,   // 新图的图像质量，取值范围：1-100
       format: 'jpg'  // 新图的输出格式，取值范围：jpg，gif，png，webp等
};
var postimg = {
    mode: 2,  // 缩略模式，共6种[0-5]
       //w: 900,   // 具体含义由缩略模式决定
       h: 800,   // 具体含义由缩略模式决定
       q: 100,   // 新图的图像质量，取值范围：1-100
       format: 'jpg'
};