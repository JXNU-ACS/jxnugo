function FileuploadUI(file) {
    this.file = file;
    
    this.filemun = 0;
    //this.fileJson = function(jarrKey){ return "\"photokey\":["+jarrKey+"]"};
    //---------------上传元素--------------
    this.uploadAreaElment = $("div[data-ariapannel=\"uploadaira\"]");
    this.uploader = "<div class='col-sm-3 show-upload' data-imgname=" + file.id + "><div class='ui-post-upload uploadimg'><a href='#'> <div class='btn btn-shadow case-in zoom-img' style='display:none;'>浏览大图</div></a><div class = 'btn btn-shadow case-in progress-img' style ='display:none;'></div> <div class='del-bg'><button type='button' class='btn-del case-in'title='删除'><spanaria-hidden='true'>&times;</span></button></div></div></div>";

    this.imgBg = ".uploadimg"
    this.uploaderElment = ".show-upload";
    this.progressStatusElement = ".progress-img";
    this.showPictureElement = '.zoom-img';
    this.delPictureElement = '.btn-del';

    this.submit = $("[name=\"submit\"]")
}

//-------------上传ui---------------

FileuploadUI.prototype.imgStatus = function(isUploading, tip) {
    var file = this.file;
    $("div[data-imgname=" + file.id + "]").find(this.progressStatusElement).attr("style", "display:block;");
    if (isUploading) {

        $("div[data-imgname=" + file.id + "]").find(this.progressStatusElement).text("上传中..."); //.height(file.loaded + "%")
    } else $("div[data-imgname=" + file.id + "]").find(this.progressStatusElement).text(tip);
};
FileuploadUI.prototype.bindUploadCancel = function(up) {
    var self = this;
    $(this.delPictureElement).click(function() {
        if (up) {
            up.removeFile(self.file);
            $("div[data-imgname=\"" + self.file.id + "\"]").remove();
            self.filemun;
        }
    })
};
FileuploadUI.prototype.crateImg = function() {
    var self = this; //然而计数器并没有实现
    if (self.filemun != 10) {
        self.uploadAreaElment.append(self.uploader);
        self.filemun += 1
    } else {
        var ui = new UI();
        ui.modalShow(function() {
            //$(".modal-body").attr("style","background-image:url("+url+");height:600px;");
            $(".modal-body").text("已达到上限") //append("<img src="+url+" width:890 >");
            $(".modal").modal('show');
        }, 0, 0)
    }
};
FileuploadUI.prototype.getJson = function(key) {
    var keystr ="";
    var json = "";
    var a = $("div[data-imgname]").length;
    a = $("div[data-imgname]").length;
    $("[name=\"submit\"]").click(function(){
    	json += "{\"photos\":[";
	    $("div[data-imgname]").each(function(index) {
	        json += "{\"key\":\"" + $(this).attr("data-key") + "\"}";
	        if (index != a - 1) json += ",";
	    });
	    json += "]}";
	    $(".imgjson").attr("value", json);
	    /*var requst = $.ajax({
	    	url:"http://www.jxnugo.com/api/new_post",
	    	contentType:"application/json;charset=utf-8",
	    	type: "POST",
	    	data:{
	    		"body":"二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，",
		        "goodName":"戴尔灵越5537",
		        "goodNum":"1",
		        "goodPrice":"2000",
		        "goodLocation":"一栋N204",
		        "goodQuality":"7成新",
		        "goodBuyTime":"2014年6月",
		        "goodTag":"1",
		        "contact":"13361640744",
		        "photos":[
		            {
		                "key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
		            },
		            {
		                "key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
		            },
		            {
		              	"key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
		            }
		        ]
		    },
		    dataType: "json",
		    statusCode: {
			    404: function() {
			      	console.log("404")
			    },
			    500:function(){
			    	console.log("500")
			    },
			    200:function(){
			    	console.log("200")
			    }
			},
			xhrFields: {
			    withCredentials: true
			}

		})*/

    })
    
    //fileJson("{\"key\":\""+key+"\"},");
    
    /*$("[name=\"submit\"]").click(function(){
        $("div[data-imgname]").each(function(index) {
        	keystr += key;
        	if (index != a-1) keystr+=":";
        });
        $(".imgjson").attr("value", keystr);
    })*/


};
//FileuploadUI.prototype.fileJson = function(jarrKey){ return "\"photokey\":["+jarrKey+"]"};
FileuploadUI.prototype.eachUpload = function(url, key) {
    var file = this.file;
    var self = this;
    $("div[data-imgname=" + file.id + "]").attr("data-key", key);
    $("div[data-imgname=" + file.id + "]").find(this.imgBg).attr("style", "background-image:url(" + url + ")").hover(function() {
        $(this).find(self.showPictureElement).toggle()

    });
    $("div[data-imgname=" + file.id + "]").find(this.showPictureElement).click(function() {
        var ui = new UI();
        ui.modalShow(function() {
            //$(".modal-body").attr("style","background-image:url("+url+");height:600px;");
            $(".modal-body").append("<img src=" + url + " width:890 >");
            $(".modal").modal('show');
        }, 1, 1)
    }); //closest("a").attr("href",url)
    $("div[data-imgname=" + file.id + "]").find(this.progressStatusElement).attr("style", "display:none;");
};



function UserImgUpload(file) {
    this.file = file;
    this.json = "";
    this.filemun = 0;
    //this.fileJson = function(jarrKey){ return "\"photokey\":["+jarrKey+"]"};
    //---------------上传元素--------------
    this.uploadAreaElment = $("#upload-aira");
    this.progressStatusElement = $(".progress");
    this.tips = $("#upload-aira").find("span");
    this.submit = $("[name=\"submit\"]");

}
UserImgUpload.prototype.imgStatus = function(isUploading, tip) {
    var self = this;
    if (isUploading) {
        self.tips.text("上传中..");
        self.progressStatusElement.height(self.file.loaded + "%")
    } else self.tips.text(tip);
};
UserImgUpload.prototype.setImg = function(url) {
    var self = this;
    self.uploadAreaElment.attr("style", "background-image:url(" + url + ")");
    $("[name='usrheadimg']").attr("value", url);
}