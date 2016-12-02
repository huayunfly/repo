function editrow(event) {
    // ctrl+c(67), ctrl+d(68), ctrl+v(86), ctrl+x(88)
    if (event.ctrlKey && 86 == event.which) {
        event.preventDefault();
        pasteRow(this);
    }
    else if (event.ctrlKey && 67 == event.which) {
        event.preventDefault();
        copyRow(this);
    }
    else if (event.ctrlKey && 68 == event.which) {
        event.preventDefault();
        deleteRow(this);
    }
}

function dragrow(md) {
    var mouseX = md.pageX;
    var mouseY = md.pageY;
    var $temprow;

    md.preventDefault();
    $temprow = $("<form class='form-horizontal span5' id='temprow'></form>").append($(this));
    $("body").append($temprow);

    $temprow.css({
        "position": "absolute",
        "top": mouseY - ($temprow.height() / 2) + "px",
        "left": mouseX - ($temprow.width() / 2) + "px",
        "opacity": "0.9"
    }).show();

    var half_row_height = ($temprow.height() / 2);
    var half_row_width = ($temprow.width() / 2);
    var $target = $("table tbody");
    var tar_pos = $target.position();
    var tops = [];
    var $target_rows = $("table tbody tr");

    $("table tbody").on("mousemove", function (mm) {
            var mm_mouseX = mm.pageX;
            var mm_mouseY = mm.pageY;

            $temprow.css({
                "top": mm_mouseY - half_row_height + "px",
                "left": mm_mouseX - half_row_width + "px"
            });
            if (mm_mouseX > tar_pos.left &&
                mm_mouseX < tar_pos.left + $target.width() + half_row_width &&
                mm_mouseY > tar_pos.top &&
                mm_mouseY < tar_pos.top + $target.height() + half_row_height
            ) {
                $target_rows.css({"border-top": "1px solid white", "border-bottom": "none"});
                tops = $.grep($target_rows, function (e) {
                    return ($(e).position().top - mm_mouseY + half_row_height > 0);
                });
                if (tops.length > 0) {
                    $(tops[0]).css("border-top", "1px solid #22aaff");
                } else {
                    if ($target_rows.length > 0) {
                        $($target_rows[$target_rows.length - 1]).css("border-bottom", "1px solid #22aaff");
                    }
                }
            } else {
                $target_rows.css({"border-top": "1px solid white", "border-bottom": "none"});
            }
        }
    );

    $("body #temprow").on("mouseup", function (mu) {
        mu.preventDefault();

        var mu_mouseX = mu.pageX;
        var mu_mouseY = mu.pageY;
        var tar_pos = $target.position();

        //$("#target .component").css({"border-top": "1px solid white", "border-bottom": "none"});

        // acting only if mouse is in right place
        if (mu_mouseX + half_row_width > tar_pos.left &&
            mu_mouseX - half_row_width < tar_pos.left + $target.width() &&
            mu_mouseY + half_row_height > tar_pos.top &&
            mu_mouseY - half_row_height < tar_pos.top + $target.height()
        ) {
            // where to add
            if (tops.length > 0) {
                $($temprow.html()).insertBefore(tops[0]);
            } else {
                $("table tbody").append($temprow.html());
            }
        } else {
            // no add
            //$("#target .component").css({"border-top": "1px solid white", "border-bottom": "none"});
            tops = [];
        }

        //clean up
        $target_rows.css({"border-top": "1px solid white", "border-bottom": "none"});
        $("table tbody").off("mousemove");
        $("#temprow").off("mouseup");
        $temprow.remove();
    });
}

function copyRow(obj) {
    var $temp;
    if (0 == $("body #clipboard").length) {
        $temp = $("<form class='form-horizontal span6' id='clipboard'></form>").append($(obj).clone());
        $temp.hide();
        $("body").append($temp);
        alert("append");
    }
    else {
        $("body #clipboard").html("<tr>" + $(obj).html() + "</tr>");
        alert("replace");
    }
}

function pasteRow(obj) {
    alert($("body #clipboard").clone().html());
    $(obj).after($("body #clipboard").clone().html());
    $(obj).next().on("keydown", editrow);
    addMask();
    addContextMenu();
    bindValidate();
    //alert($("table tbody tr:last").html());
    rename();
}

function deleteRow(obj) {
    if ($(obj).siblings().length > 0) {
        $(obj).remove();
    }
    rename();
}

function newRow(obj) {

}

function rename() {
    $("table tbody tr").each(function (index) {
        var day = $("td select[name$='daySel']");
        var project = $("td select[name$='projectSel']");
        var tasktime = $("td input[name$='percentageInput']");
        $(this).find(day).attr('name', 'form-' + index + '-daySel');
        $(this).find(day).attr('id', 'id_form-' + index + '-daySel');
        $(this).find(project).attr('name', 'form-' + index + '-projectSel');
        $(this).find(project).attr('id', 'id_form-' + index + '-projectSel');
        $(this).find(tasktime).attr('name', 'form-' + index + '-percentageInput');
        $(this).find(tasktime).attr('id', 'id_form-' + index + '-percentageInput');
    });
}

// Validate the user task input.
// The task day and time are saved in two correlative arrays which combine to a mapping.
// We check the user input digital number as the task time.
// Under any given day, the tasks total time can not be larger than 1.0. When the validation
// is failed, the input box border will be highlighted using Bootstrap.
function validate() {
    var days = [];
    var times = [];
    var DELIMITER = '_';
    $("table tbody tr").each(function (index) {
        var $day = $("td select[name$='daySel']");
        var $tasktime = $("td input[name$='percentageInput']");
        var day = $(this).find($day).val();
        // Strip '%' in the tasktime if it has some.
        var tasktime = String($(this).find($tasktime).val()).replace(/%/, "");
        var has_error = false;
        var val;
        if (!isInteger(tasktime)) {
            has_error = true;
        }
        else {
            val = parseInt(tasktime);
            if (val < 0 || val > 100) {
                has_error = true;
            }
        }

        if (!has_error) {
            var index = getArrayIndex(days, day);
            if (index >= 0) {
                if (times[index] + val > 100) {
                    has_error = true;
                }
                else {
                    times[index] += val;
                }
            }
            else {
                days[days.length] = day;
                times[times.length] = val;
                index = times.length
            }
            // Re-format 'Mon, Nov 28' to 'Mon_Nov_28' matching the progress bar id.
            // Get week number in 'Mon, Nov 28' as 'Mon'
            var progress_id = day.replace(/\s+/g, DELIMITER).replace(',', '');
            var suffix = day.split(',')[0];
            setProgress(progress_id, times[index], convertWeekdayName(suffix));
        }

        if (has_error) {
            $(this).find($tasktime).parent().attr("class", "has-error");
        }
        else {
            $(this).find($tasktime).parent().attr("class", null);
        }
    });
}

// Set the progress bar element content
// @param progress_id: the progress bar element ID
// @param percent: the progress range [0, 100]
// @param suffix: displaying suffix adding after 'percent%', such as 100% Mon, where the suffix is 'Mon'
function setProgress(progress_id, percent, suffix) {
    var $progress = $("#" + progress_id);
    $progress.find(".progress-bar").attr("aria-valuenow", percent);
    $progress.find(".progress-bar").attr("style", "width:" + percent + "%;");
    $progress.find(".progress-bar span").text(percent + '%' + suffix);
}

// Convert the week day name to another. For example: Mon -> 周一
// @param day_name: the original weekday name.
// @return converted name, 周一 e.g. If there is no match, return empty a string ''.
function convertWeekdayName(day_name)
{
    var day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    var converted = ['周一','周二','周三','周四','周五','周六','周日'];
    var index = getArrayIndex(day_names, day_name);
    if (index >= 0)
    {
        return converted[index];
    }
    else
    {
        return '';
    }
}

function isFloat(str) {
    if (/^(-?\d+)(\.\d+)?$/.test(str)) {
        return true;
    }
    return false;
}

// Search a key in an array and return the key index.
// @param arr: the array
// @param key: the searching key
// @return: -1 if it is failed, otherwise the key index
function getArrayIndex(arr, key) {
    var index = -1;
    for (var i = 0; i < arr.length; i++) {
        if (key == arr[i]) {
            index = i;
            break;
        }
    }
    return index;
}

function isInteger(str) {
    if (/^-?\d+$/.test(str)) {
        return true;
    }
    return false;
}

// Add percentage mask for the input
function addMask() {
    $("input[name$='percentageInput']").mask('##000%', {reverse: true});
    //$("input[name$='percentageInput']").each(function () {
    //    $(this).mask('##000%', {reverse: true});
    //});
}

// Bind task time validate to input elements
function bindValidate() {
    $("table tbody tr input").change(function () {
        validate();
    });
}

// Add a context menu for the each tasktime row.
function addContextMenu() {
    $("tr").contextmenu({
        target: '#context-menu',
        before: function (e, context) {
            // execute code before context menu if shown
        },
        onItem: function (context, e) {
            // context is this
            var index = $(e.currentTarget).find("a").attr("tabindex");
            if (0 == index) {
                copyRow(context);
            }
            else if (1 == index) {
                pasteRow(context);
            }
            else if (2 == index) {
                deleteRow(context);
            }
            else if (3 == index) {
                newRow(context);
            }
        }
    });
}


$(document).ready(function () {
    $("table tbody tr").on("keydown", editrow);
    $("#targettest").click(function () {
        validate();
    });
    addMask();
    addContextMenu();
    bindValidate();
    validate();
    //$("table tbody tr").on("mousedown", dragrow);
});


/*$(document).ready(function () {
 $("table tbody tr").on("keydown", editrow);

 $("form .component").on("mousedown", function (md) {
 //$(".popover").remove();

 // md.preventDefault();
 var tops = [];
 var mouseX = md.pageX;
 var mouseY = md.pageY;
 var $temp;
 var timeout;
 var $this = $(this);
 var delays = {
 main: 0,
 form: 120
 }
 var type;

 if ($this.parent().parent().parent().parent().attr("id") === "components") {
 type = "main";
 } else {
 type = "form";
 }

 var delayed = setTimeout(function () {
 if (type === "main") {
 $temp = $("<form class='form-horizontal span6' id='temp'></form>").append($this.clone());
 } else {
 if ($this.attr("id") !== "legend") {
 $temp = $("<form class='form-horizontal span6' id='temp'></form>").append($this);
 }
 }

 $("body").append($temp);

 // Temporarily display in UI (<body>)
 $temp.css({
 "position": "absolute",
 "top": mouseY - ($temp.height() / 2) + "px",
 "left": mouseX - ($temp.width() / 2) + "px",
 "opacity": "0.9"
 }).show();

 var half_box_height = ($temp.height() / 2);
 var half_box_width = ($temp.width() / 2);
 var $target = $("#target");
 var tar_pos = $target.position();
 var $target_component = $("#target .component");

 $("body").on("mousemove", function (mm) {

 var mm_mouseX = mm.pageX;
 var mm_mouseY = mm.pageY;

 $temp.css({
 "top": mm_mouseY - half_box_height + "px",
 "left": mm_mouseX - half_box_width + "px"
 });

 if (mm_mouseX > tar_pos.left &&
 mm_mouseX < tar_pos.left + $target.width() + $temp.width() / 2 &&
 mm_mouseY > tar_pos.top &&
 mm_mouseY < tar_pos.top + $target.height() + $temp.height() / 2
 ) {
 $("#target").css("background-color", "#fafdff");
 $target_component.css({"border-top": "1px solid white", "border-bottom": "none"});
 tops = $.grep($target_component, function (e) {
 return ($(e).position().top - mm_mouseY + half_box_height > 0 && $(e).attr("id") != "legend");
 });
 if (tops.length > 0) {
 $(tops[0]).css("border-top", "1px solid #22aaff");
 } else {
 if ($target_component.length > 0) {
 $($target_component[$target_component.length - 1]).css("border-bottom", "1px solid #22aaff");
 }
 }
 } else {
 $("#target").css("background-color", "#fff");
 $target_component.css({"border-top": "1px solid white", "border-bottom": "none"});
 $target.css("background-color", "#fff");
 }
 });

 $("body #temp").on("mouseup", function (mu) {
 mu.preventDefault();

 var mu_mouseX = mu.pageX;
 var mu_mouseY = mu.pageY;
 var tar_pos = $target.position();

 $("#target .component").css({"border-top": "1px solid white", "border-bottom": "none"});

 // acting only if mouse is in right place
 if (mu_mouseX + half_box_width > tar_pos.left &&
 mu_mouseX - half_box_width < tar_pos.left + $target.width() &&
 mu_mouseY + half_box_height > tar_pos.top &&
 mu_mouseY - half_box_height < tar_pos.top + $target.height()
 ) {
 $temp.attr("style", null);
 // where to add
 if (tops.length > 0) {
 $($temp.html()).insertBefore(tops[0]);
 } else {
 $("#target .component").append($temp.append("\n\n\ \ \ \ ").html());
 }
 } else {
 // no add
 $("#target .component").css({"border-top": "1px solid white", "border-bottom": "none"});
 tops = [];
 }

 //clean up & add popover
 $target.css("background-color", "#fff");
 $("body").off("mousemove");
 $("#temp").off("mouseup");
 $("#target .component").popover({trigger: "manual"});
 //$temp.remove();
 genSource();
 });
 }, delays[type]);

 $(document).mouseup(function () {
 clearInterval(delayed);
 return false;
 });
 $(this).mouseout(function () {
 clearInterval(delayed);
 return false;
 });
 });

 var genSource = function () {
 var $temptxt = $("<div>").html($("#build").html());
 //scrubbbbbbb
 $($temptxt).find(".component").attr({
 "title": null,
 "data-original-title": null,
 "data-type": null,
 "data-content": null,
 "rel": null,
 "trigger": null,
 "style": null
 });
 $($temptxt).find(".valtype").attr("data-valtype", null).removeClass("valtype");
 $($temptxt).find(".component").removeClass("component");
 $($temptxt).find("form").attr({"id": null, "style": null});
 $("#source").val($temptxt.html().replace(/\n\ \ \ \ \ \ \ \ \ \ \ \ /g, "\n"));
 }

 //activate legend popover
 $("#target .component").popover({trigger: "manual"});
 //popover on click event
 $("#target").off(".component", "click", function (e) {
 e.preventDefault();
 $(".popover").hide();
 var $active_component = $(this);
 $active_component.popover("show");
 var valtypes = $active_component.find(".valtype");
 $.each(valtypes, function (i, e) {
 var valID = "#" + $(e).attr("data-valtype");
 var val;
 if (valID === "#placeholder") {
 val = $(e).attr("placeholder");
 $(".popover " + valID).val(val);
 } else if (valID === "#checkbox") {
 val = $(e).attr("checked");
 $(".popover " + valID).attr("checked", val);
 } else if (valID === "#option") {
 val = $.map($(e).find("option"), function (e, i) {
 return $(e).text()
 });
 val = val.join("\n")
 $(".popover " + valID).text(val);
 } else if (valID === "#checkboxes") {
 val = $.map($(e).find("label"), function (e, i) {
 return $(e).text().trim()
 });
 val = val.join("\n")
 $(".popover " + valID).text(val);
 } else if (valID === "#radios") {
 val = $.map($(e).find("label"), function (e, i) {
 return $(e).text().trim()
 });
 val = val.join("\n");
 $(".popover " + valID).text(val);
 $(".popover #name").val($(e).find("input").attr("name"));
 } else if (valID === "#inline-checkboxes") {
 val = $.map($(e).find("label"), function (e, i) {
 return $(e).text().trim()
 });
 val = val.join("\n")
 $(".popover " + valID).text(val);
 } else if (valID === "#inline-radios") {
 val = $.map($(e).find("label"), function (e, i) {
 return $(e).text().trim()
 });
 val = val.join("\n")
 $(".popover " + valID).text(val);
 $(".popover #name").val($(e).find("input").attr("name"));
 } else if (valID === "#button") {
 val = $(e).text();
 var type = $(e).find("button").attr("class").split(" ").filter(function (e) {
 return e.match(/btn-.*!/)
 });
 $(".popover #color option").attr("selected", null);
 if (type.length === 0) {
 $(".popover #color #default").attr("selected", "selected");
 } else {
 $(".popover #color #" + type[0]).attr("selected", "selected");
 }
 val = $(e).find(".btn").text();
 $(".popover #button").val(val);
 } else {
 val = $(e).text();
 $(".popover " + valID).val(val);
 }
 });

 $(".popover").delegate(".btn-danger", "click", function (e) {
 e.preventDefault();
 $active_component.popover("hide");
 });

 $(".popover").delegate(".btn-info", "click", function (e) {
 e.preventDefault();
 var inputs = $(".popover input");
 inputs.push($(".popover textarea")[0]);
 $.each(inputs, function (i, e) {
 var vartype = $(e).attr("id");
 var value = $active_component.find('[data-valtype="' + vartype + '"]')
 if (vartype === "placeholder") {
 $(value).attr("placeholder", $(e).val());
 } else if (vartype === "checkbox") {
 if ($(e).is(":checked")) {
 $(value).attr("checked", true);
 }
 else {
 $(value).attr("checked", false);
 }
 } else if (vartype === "option") {
 var options = $(e).val().split("\n");
 $(value).html("");
 $.each(options, function (i, e) {
 $(value).append("\n      ");
 $(value).append($("<option>").text(e));
 });
 } else if (vartype === "checkboxes") {
 var checkboxes = $(e).val().split("\n");
 $(value).html("\n      <!-- Multiple Checkboxes -->");
 $.each(checkboxes, function (i, e) {
 if (e.length > 0) {
 $(value).append('\n      <label class="checkbox">\n        <input type="checkbox" value="' + e + '">\n        ' + e + '\n      </label>');
 }
 });
 $(value).append("\n  ")
 } else if (vartype === "radios") {
 var group_name = $(".popover #name").val();
 var radios = $(e).val().split("\n");
 $(value).html("\n      <!-- Multiple Radios -->");
 $.each(radios, function (i, e) {
 if (e.length > 0) {
 $(value).append('\n      <label class="radio">\n        <input type="radio" value="' + e + '" name="' + group_name + '">\n        ' + e + '\n      </label>');
 }
 });
 $(value).append("\n  ")
 $($(value).find("input")[0]).attr("checked", true)
 } else if (vartype === "inline-checkboxes") {
 var checkboxes = $(e).val().split("\n");
 $(value).html("\n      <!-- Inline Checkboxes -->");
 $.each(checkboxes, function (i, e) {
 if (e.length > 0) {
 $(value).append('\n      <label class="checkbox inline">\n        <input type="checkbox" value="' + e + '">\n        ' + e + '\n      </label>');
 }
 });
 $(value).append("\n  ")
 } else if (vartype === "inline-radios") {
 var radios = $(e).val().split("\n");
 var group_name = $(".popover #name").val();
 $(value).html("\n      <!-- Inline Radios -->");
 $.each(radios, function (i, e) {
 if (e.length > 0) {
 $(value).append('\n      <label class="radio inline">\n        <input type="radio" value="' + e + '" name="' + group_name + '">\n        ' + e + '\n      </label>');
 }
 });
 $(value).append("\n  ")
 $($(value).find("input")[0]).attr("checked", true)
 } else if (vartype === "button") {
 var type = $(".popover #color option:selected").attr("id");
 $(value).find("button").text($(e).val()).attr("class", "btn " + type);
 } else {
 $(value).text($(e).val());
 }
 $active_component.popover("hide");
 genSource();
 });
 });
 });
 $("#navtab").delegate("#sourcetab", "click", function (e) {
 genSource();
 });
 });*/
