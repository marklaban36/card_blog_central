const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/*
 * Initializes edit functionality for the provided edit buttons.
 */
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    const commentId = e.target.getAttribute("data-comment_id");
    const commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}

/*
 * Initializes deletion functionality for the provided delete buttons.
 */
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    const commentId = button.getAttribute("data-comment-id");
    const postSlug = button.getAttribute("data-post-slug");

    if (commentId && postSlug) {
      const deleteUrl = `/post/${postSlug}/comment/${commentId}/delete/`;
      deleteConfirm.setAttribute("href", deleteUrl);
      deleteModal.show();
    } else {
      console.error("Missing commentId or postSlug on delete button");
    }
  });
}
