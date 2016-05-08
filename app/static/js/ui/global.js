function UI() {
    //...这里可以存放jq对象的［元素］
    //气泡提示
    this.tooltipElement = $('[data-toggle="tooltip"]');
    //模态框
    this.modalElement = $(".modal");
    //跟随父级容器固定在浏览器上的
    this.stickyElement = $(".stickypannel");
    //选择标签
    this.selectTagElement = $(".select");
    //测试是否支持的css属性
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
}
UI.prototype.bubbleTip = function() {
        this.tooltipElement.tooltip();
    }
    //模态框
UI.prototype.modalShow = function(messages) {
    var a;
    var b = this.modalElement;
    b.modal({
        keyboard: false,
        show: false
    }).on("shown.bs.modal", function() {
        a = setInterval(function() {
            b.modal('hide')
        }, 3000)
    }).on("hidden.bs.modal", function() {
        clearInterval(a)
    }).ready(messages);
};
/*选择标签(tag)指向类(class)“.select”
id指向作用面板
data-ariapannel 被作用面板
.select外需要包含div［不写都不造自己写的什么了orz
*/
UI.prototype.slideBlock = function(config) { //config为object
    var a = config.originPosition;
    setSlideBlockState($(a))

    function setSlideBlockState(a) {
        var offset = (a.closest("div").position().left - a.closest("div").parent().find("div:first-child").position().left) + (a.closest("div").innerWidth() / 2) - 47
        $(".slideBlock").css("left", offset)
            //console.log(a.closest("div").parent().find("div:first-child").position().left)
    }
    this.selectTagElement.click(function() {
        //页面切换选择器（
        var b = $(this).attr("id")
        a = "#" + b
        setSlideBlockState($(this))
        $("div[data-ariapannel]").each(function() {
            $(this).attr("data-ariapannel") == b ? $(this).attr("style", "") : $(this).attr("style", "display:none;")
        })
    })
    this.selectTagElement.hover(function() {
        setSlideBlockState($(this))
    }, function() {
        setSlideBlockState($(a))
    })
};
//仅作用于trade_list，能复用的时候再改吧
UI.prototype.listToggle = function() {
    var s = 0
    $('.btn-list-toggle').click(function() {
        if (s == 1) {
            $(".ui-trade-show").removeClass("contain-shrink").addClass("contain-extend")
            $(".ui-trade-show-contain-headbg").removeClass("fade-out").addClass("fade-in")
            s = 0
        } else {
            $(".ui-trade-show").removeClass("contain-extend").addClass("contain-shrink")
            $(".ui-trade-show-contain-headbg").removeClass("fade-in").addClass("fade-out")
            s = 1
        }
    })
};
UI.prototype.sticky = function(config) {
    var a = config.offsetY;
    var b = config.contain;//jq选择对象
    if (this.isSupportSticky) {
        this.stickyElement.attr('style', "position:-webkit-sticky;position:sticky;top:" + a + "px;")
        console.log("1")
    } else {
        var Offset = b.offset();

        function onScroll(e) {
            window.scrollY >= Offset.top ? b.css({position:"fixed"}) : b.css({position:""});
        }
        window.addEventListener('scroll', onScroll);
        console.log("2")
    }
};