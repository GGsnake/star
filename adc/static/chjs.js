
        function deletee(obj) {
            var id = obj.name;
            $(document).ready(function () {

                var con;
                con = confirm("确定删除么?");
                if (con == true)
                    $.ajax({
                        url: "chdeletfirbe/",
                        data: {id: id},
                        success: function (data) {

                            alert("删除成功")
                            $('#' + id).empty()
                            window.location.reload()
                        }

                    })


            });


        };

        function deleteef(obj) {
            var id = obj.name;
            $(document).ready(function () {

                var con;
                con = confirm("确定删除么?");
                if (con == true)
                    $.ajax({
                        url: "chdeletfirbe/",
                        data: {id: id},
                        success: function (data) {

                            alert("删除成功")
                            $('#' + id).empty()

                        }

                    })


            });


        };

        $(document).ready(function () {
            $("#quee").click(function () {

                if ($("#protect").val() != "") {
                    var pro = $("#protect").val();
                }
                if ($("#firenumber").val() != "") {
                    var fis = $("#firenumber").val();
                }

                $.ajax({
                    url: "QureyChannel/",

                    data: {channel: fis, protect: pro, protect: pro},
                    success: function (data) {
                        $('#tabb').empty()
                        jQuery.each(data, function (i, item) {
                            $('#tabb').append(" <tr id=\"" + item.Channelname + "\">\n" +
                                "                        <th>" + "<input type=\"checkbox\" id=\"checkAll\" name=\"checkAll\"/>" + "</th>\n" +
                                "                        <th>" + "<a href='ChShow?id=" + item.Channelname + "'>" + item.Channelname + "</a>" + "</th>\n" +
                                "                        <th>" + item.Firbenumber + "</th>\n" +
                                "                        <th>" + item.Mainman + "</th>\n" +

                                "                        <th>" + " <button type=\"button\" name=\"" + item.Channelname + "\"\n" +
                                "                                            class=\"btn btn-default btn-sm\"><a\n" +
                                "                                            href='chupdate?id=" + item.Channelname + "'>修改</a>\n" +
                                "                                    </button>" + "  <button type=\"button\"  onclick=\"deleteef(this)\" name=\"" + item.Channelname + "\" class=\"btn btn-default btn-sm\">删除</button>\n"
                                +
                                "                        </button>" + "</th>\n" +

                                "                    </tr>"
                            )
                        });
                    }
                })
            });

        });