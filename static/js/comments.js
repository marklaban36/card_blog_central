document.addEventListener("DOMContentLoaded", function () {
  var editButtons = document.querySelectorAll(".btn-edit");
  var commentText = document.getElementById("id_body");
  var commentForm = document.getElementById("commentForm");
  var submitButton = document.getElementById("submitButton");

  var deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  var deleteButtons = document.querySelectorAll(".btn-delete");
  var deleteConfirm = document.getElementById("deleteConfirm");

  // Edit functionality
  Array.prototype.forEach.call(editButtons, function (button) {
    button.addEventListener("click", function (e) {
      var commentId = e.currentTarget.dataset.comment_id;

      requestAnimationFrame(function () {
        var commentElement = document.getElementById("comment" + commentId);
        if (commentElement) {
          var commentContent = commentElement.textContent.trim();

          commentText.value = commentContent;
          submitButton.textContent = "Update";
          commentForm.action = "edit_comment/" + commentId;
        }
      });
    });
  });

  // Delete functionality
  Array.prototype.forEach.call(deleteButtons, function (button) {
    button.addEventListener("click", function (e) {
      var commentId = e.currentTarget.dataset.commentId;
      var postSlug = e.currentTarget.dataset.postSlug;

      if (commentId && postSlug) {
        deleteConfirm.href = "/post/" + postSlug + "/comment/" + commentId + "/delete/";
        deleteModal.show();
      } else {
        console.error("Missing commentId or postSlug on delete button");
      }
    });
  });
});
