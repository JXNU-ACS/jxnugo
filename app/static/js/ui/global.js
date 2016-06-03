function UI() {
    //跟随父级容器固定在浏览器上的
    this.stickyElement = $(".stickypannel");
    //选择标签
    this.selectTagElement = $(".select");
    
    this.bubbleTip = function() {
        $('[data-toggle="tooltip"]').tooltip();
    }
    //测试是否支持的css属性(sticky)
    this.isSupportSticky = function() {
        var prefixTestList = ['', '-webkit-', '-ms-', '-moz-', '-o-'];
        var stickyText = '';
        for (var i = 0; i < prefixTestList.length; i++) {
            stickyText += 'position:' + prefixTestList[i] + 'sticky;';
        }
        // 创建一个dom来检查
        var div = document.createElement('div');
        var body = document.body;
        div.style.cssText = 'display:none;' + stickyText;
        body.appendChild(div);
        var isSupport = /sticky/i.test(window.getComputedStyle(div).position);
        body.removeChild(div);
        div = null;
        return isSupport;
    };
    this.modalShow = function(func,time,isbig) {
        var a;
        var b = $(".modal");
        var c;
        (isbig)?b.find(".modal-dialog").removeClass("modal-sm").addClass("modal-lg"):b.find(".modal-dialog").addClass("modal-sm").removeClass("modal-lg");
        b.modal({
            keyboard: false,
            show: false
        }).on("shown.bs.modal", function() {
            if(time == 0){
                a = setInterval(function() {
                    b.modal('hide')
                }, 3000)
                c=1;
            }
            
        }).on("hidden.bs.modal", function() {
            if(c){
                clearInterval(a);
            }
            $(".modal-body").empty()
        }).ready(func);
    };
    //表单验证器(jqattr指表单form)
    this.formValidation = function(jqattr){
        var self = this;
        jqattr.submit(function(){
            if(self.difFormTip(jqattr))return true;
            else return false;
        })
        
    };
    //不同的表单验证提示
    this.difFormTip = function(jqattr){
        var tips = "";
        var offset = "padding: 5% 0;right:10px"
        var is_ok = true;
        jqattr.find('[require="true"]').each(function(){
            $(this).nextAll("span").remove();
                if($(this).val() == "" || $(this).val()== null || $(this).val() == false ||$('[name="regpassWord"]').val() != $('[name="confirm"]').val()){
                    if($(this).attr("type") == "text") tips = "没填写的说";
                    if($(this).attr("type") == "checkbox"){
                        tips = "没选择的说";
                        offset = "padding:0 25px";
                    }
                    if($(this).attr("type") == "password"){
                        if($(this).val() == "" || $(this).val()== null) tips = "傻屌忘记输密码啦！";
                        if($('[name="regpassWord"]').val() != $('[name="confirm"]').val()) tips = "傻屌这个和下面不一样";
                    }
                    $(this).attr("style","border-color:#FF7C6A;").focusin(function(){
                        $(this).nextAll("span").remove();
                    })
                    $(this).parent().append("<span style='color:#FF7C6A;position: absolute;white-space: nowrap;"+offset+"'>"+tips+"</span>")
                    is_ok = false;
                }else{
                    $(this).attr("style","border-color:#eee;")
                }
        })
        return is_ok;
    };

}
/*选择标签(tag)指向类(class)“.select”
id指向作用面板
data-ariapannel 被作用面板
.select外需要包含div［不写都不造自己写的什么了orz
*/
//目前不能在同一页面实现两个实例～
UI.prototype.slideBlock = function(config) { //config为object
    var a = config.originPosition; //id
    var b = config.slideBlock; //滑块的类
    var self = this;
    setposition($(a))

    function setposition(a) {
        var offset = (a.closest("div").position().left - a.closest("div").parent().find("div:first-child").position().left) + (a.closest("div").innerWidth() / 2) - 47
        $(b).css("left", offset)
            //console.log(a.closest("div").parent().find("div:first-child").position().left)
    }
    self.selectTagElement.click(function() {
        setposition($(this));
        a = self.selectPannel($(this));
    })
    self.selectTagElement.hover(function() {
        setposition($(this))
    }, function() {
        setposition($(a))
    })
};
//.jqobj 任意id名选择标签（这个是个大坑)
UI.prototype.selectPannel = function(jqobj){
        //页面切换选择器（
        var b = jqobj.attr("id")
        a = "#" + b;
        $("div[data-ariapannel]").each(function() {
            $(this).attr("data-ariapannel") == b ? $(this).attr("style", "") : $(this).attr("style", "display:none;")
        })
        return a;
}
//在支持的但是没开启的浏览器下有bug
UI.prototype.sticky = function(config) {
    var a = config.offsetY;
    var b = config.contain; //jq选择对象
    var self = this;
    if (self.isSupportSticky) {
        self.stickyElement.attr('style', "position:-webkit-sticky;position:sticky;top:" + a + "px;")

   } else {
        var Offset = b.offset();

        function onScroll(e) {
            window.scrollY >= Offset.top ? self.stickyElement.attr("style","position:fixed;top:"+a+"px;") : self.stickyElement.attr("style","position:relative");
        }
        window.addEventListener('scroll', onScroll);

   }
};


