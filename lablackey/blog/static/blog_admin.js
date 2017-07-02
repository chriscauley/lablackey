/**
* Field Defenitions
*/
// html elements
var el_publish_dt_wrap = $('#date');
var el_slug_helper = $('#slug-helper');

// form fields
var f_title = $('#id_title');
var f_content = $('#id_content');
var f_slug = $('#id_slug');
var f_publish_dt = $('#id_publish_dt');
var f_status = $('#id_status');
var f_token = $('input[name="csrfmiddlewaretoken"]');
/**
* Content Inserts
*/
$(".media-item a").click(function(){
    $("#id_content").insertAtCaret($(this).attr('data-shortcode'));
    return false;
});


/**
* Tooltips
*/
$('a[rel=tooltip]').tooltip();

/**
* Preview Mode
**/
function show_preview(xhr, status) {
    if (status == 'success') {
        var el_preview = $('#preview-modal');
        var html = xhr.responseText;
        el_preview.find('.modal-body').html(html);
        el_preview.modal();
    }
}

function query_preview() {
    var url = '/admin/preview/';
    var data = {
        title: f_title.val(),
        content: f_content.val(),
        csrfmiddlewaretoken: f_token.val()
    }

    $.ajax(url, {
        type: 'POST',
        data: data,
        complete: function(xhr, status) {
            show_preview(xhr, status);
        }
    });
}

$(document).bind('keydown', 'ctrl+shift+q', query_preview);
f_title.bind('keydown', 'ctrl+shift+q', query_preview);
f_content.bind('keydown', 'ctrl+shift+q', query_preview);
f_slug.bind('keydown', 'ctrl+shift+q', query_preview);

if (document.querySelector("#blogForm #id_content")) {
  var insert_photo = {
    name: "insert-photo",
    action: function customFunction(editor){
      var cm = editor.codemirror;
      insertImage(cm.getSelection(),function(result) {
        cm.replaceSelection(result.shortcode);
      })
    },
    className: "fa fa-star",
    title: "Custom Button",
  };
  new SimpleMDE({
    element: document.querySelector("textarea"),
    spellChecker: false,
    toolbar: [
      'bold','italic','heading','|',
      'quote','unordered-list','ordered-list','|',
      'link', insert_photo, "|",
      'preview','side-by-side','fullscreen',"|",
    ],
  });
};

