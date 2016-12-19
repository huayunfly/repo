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
    else if (event.ctrlKey && 78 == event.which) {
        event.preventDefault();
        newRow();
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
    var $src = obj;
    var $cloned = $src.clone();
    $cloned.find("td select[name$='daySel']").get(0).selectedIndex =
        $src.find("td select[name$='daySel']").get(0).selectedIndex;
    $cloned.find("td select[name$='projectSel']").get(0).selectedIndex =
        $src.find("td select[name$='projectSel']").get(0).selectedIndex;

    var $clipboard = $("body #clipboard");
    if (0 == $clipboard.length) {
        var $temp;
        $temp = $("<form class='form-horizontal span6' id='clipboard'></form>").append($cloned);
        $temp.hide();
        $("body").append($temp);
        //alert("append");
    }
    else {
        $clipboard.empty();
        $clipboard.append($cloned);
        //alert("replace");
    }
}

function pasteRow(obj) {
    var $src = $("body #clipboard").children().first();
    var $cloned = $src.clone();
    $cloned.find("td select[name$='daySel']").get(0).selectedIndex =
        $src.find("td select[name$='daySel']").get(0).selectedIndex;
    $cloned.find("td select[name$='projectSel']").get(0).selectedIndex =
        $src.find("td select[name$='projectSel']").get(0).selectedIndex;

    $(obj).after($cloned);
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

function newRow() {
    var $rows = $("table tbody tr");
    var $src = $rows.first();
    var $cloned = $src.clone();
    $cloned.find("td select[name$='daySel']").get(0).selectedIndex =
        $src.find("td select[name$='daySel']").get(0).selectedIndex;
    $cloned.find("td select[name$='projectSel']").get(0).selectedIndex =
        $src.find("td select[name$='projectSel']").get(0).selectedIndex;

    $rows.last().after($cloned);
    // $rows query will not be updated automatically. So $rows.last().next() is used.
    $rows.last().next().find("input[name$='percentageInput']").val("0%");
    addMask();
    addContextMenu();
    bindValidate();
    rename();
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
// @return has_error: true or false.
function validate() {
    var days = [];
    var times = [];
    var DELIMITER = '_';
    var has_error = false;
    clearProgress();
    $("table tbody tr").each(function (index) {
        var $day = $("td select[name$='daySel']");
        var $tasktime = $("td input[name$='percentageInput']");
        var day = $(this).find($day).val();
        // Strip '%' in the tasktime if it has some.
        var tasktime = String($(this).find($tasktime).val()).replace(/%/, "");
        //var has_error = false;
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
                days.push(day);
                times.push(val);
                index = times.length - 1;
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
    return has_error;
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

// Clear all progress bars to zero.
function clearProgress() {
    var $progress_bar = $(".progress-bar");
    $progress_bar.attr("aria-valuenow", 0);
    $progress_bar.attr("style", "width:0%;");
    $progress_bar.find("span").text("0%");
}

// Convert the week day name to another. For example: Mon -> 周一
// @param day_name: the original weekday name.
// @return converted name, 周一 e.g. If there is no match, return empty a string ''.
function convertWeekdayName(day_name) {
    var day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    var converted = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
    var index = getArrayIndex(day_names, day_name);
    if (index >= 0) {
        return converted[index];
    }
    else {
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

    $("#btn_new_row").click(function () {
        newRow();
    });
    $("form").submit(function (event) {
        if (!validate()) {
            return;
        }

        $("#validate_msg").text("保存失败: 单日工时合计应不超过100%.").show().fadeOut(5000);
        event.preventDefault();
    });


    addMask();
    addContextMenu();
    bindValidate();
    validate();
    //$("table tbody tr").on("mousedown", dragrow);
});
