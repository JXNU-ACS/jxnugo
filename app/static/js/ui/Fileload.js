function FileuploadUI(file){
	this.file = file;
	this.json = "";
	this.filemun = 0;
	//this.fileJson = function(jarrKey){ return "\"photokey\":["+jarrKey+"]"};
	//---------------上传元素--------------
    this.uploadAreaElment = $("div[data-ariapannel=\"uploadaira\"]");
    this.uploader = "<div class='col-sm-3 show-upload' data-imgname="+file.id+"><div class='ui-post-upload uploadimg'><a href='#'> <div class='btn btn-shadow case-in zoom-img' style='display:none;'>浏览大图</div></a><div class = 'btn btn-shadow case-in progress-img' style ='display:none;'></div> <div class='del-bg'><button type='button' class='btn-del case-in'title='删除'><spanaria-hidden='true'>&times;</span></button></div></div></div>";

    this.imgBg = ".uploadimg"
    this.uploaderElment = ".show-upload";
    this.progressStatusElement = ".progress-img";
    this.showPictureElement = '.zoom-img';
    this.delPictureElement = '.btn-del';

    this.submit = $("[name=\"submit\"]")
}

//-------------上传ui---------------

FileuploadUI.prototype.imgStatus = function(isUploading,tip) {
	var file = this.file;
	$("div[data-imgname="+file.id+"]").find(this.progressStatusElement).attr("style","display:block;");
    if (isUploading) {
    	
        $("div[data-imgname="+file.id+"]").find(this.progressStatusElement).text("上传中...");//.height(file.loaded + "%")
    } else $("div[data-imgname="+file.id+"]").find(this.progressStatusElement).text(tip);
};
FileuploadUI.prototype.bindUploadCancel = function(up) {
	var self = this;
	$(this.delPictureElement).click(function(){
		if (up) {
        up.removeFile(self.file);
        $("div[data-imgname=\""+self.file.id+"\"]").remove();
    	self.filemun;
    	}
	})
};
FileuploadUI.prototype.crateImg = function() {
	var self = this;//然而计数器并没有实现
    if(self.filemun !=10) {
    	self.uploadAreaElment.append(self.uploader);
    	self.filemun +=1
    }
    else {
    	var ui = new UI();
		ui.modalShow(function(){
			//$(".modal-body").attr("style","background-image:url("+url+");height:600px;");
			$(".modal-body").text("已达到上限")//append("<img src="+url+" width:890 >");
			$(".modal").modal('show');
		},0,0)
    }
};
FileuploadUI.prototype.getJson = function(key){
	var self = this;
	var a;

	self.submit.click(function(){
		a = $("div[data-imgname]").length;
		self.json += "\"photokey\":[";
		$("div[data-imgname]").each(function(index){
			self.json += "{\"key\":\""+$(this).attr("data-key")+"\"}";
			if (index != a-1) self.json +=",";
		});
		self.json += "]";
		
		//self.fileJson("{\"key\":\""+key+"\"},");
		$(".imgjson").attr("value",self.json);
	});
	
	
};
//FileuploadUI.prototype.fileJson = function(jarrKey){ return "\"photokey\":["+jarrKey+"]"};
FileuploadUI.prototype.eachUpload = function(url,key){
	var file = this.file;
	var self = this;
	$("div[data-imgname="+file.id+"]").attr("data-key",key);
	$("div[data-imgname="+file.id+"]").find(this.imgBg).attr("style","background-image:url("+url+")").hover(function() {
        $(this).find(self.showPictureElement).toggle()

    });
	$("div[data-imgname="+file.id+"]").find(this.showPictureElement).click(function(){
		var ui = new UI();
		ui.modalShow(function(){
			//$(".modal-body").attr("style","background-image:url("+url+");height:600px;");
			$(".modal-body").append("<img src="+url+" width:890 >");
			$(".modal").modal('show');
		},1,1)
	});//closest("a").attr("href",url)
	$("div[data-imgname="+file.id+"]").find(this.progressStatusElement).attr("style","display:none;");
};



function UserImgUpload(file){
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
UserImgUpload.prototype.imgStatus = function(isUploading,tip){
	var self = this;
    if (isUploading) {
        self.tips.text("上传中..");
        self.progressStatusElement.height(self.file.loaded + "%")
    } else self.tips.text(tip);
};
UserImgUpload.prototype.setImg = function(url){
	var self = this;
	self.uploadAreaElment.attr("style","background-image:url("+url+")");
	$("[name='usrheadimg']").attr("value",url);
}