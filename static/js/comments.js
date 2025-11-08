document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.getElementsByClassName("btn-edit");
  const commentText = document.getElementById("id_body");
  const commentForm = document.getElementById("commentForm");
  const submitButton = document.getElementById("submitButton");

  const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteConfirm = document.getElementById("deleteConfirm");

  // Edit functionality
  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      const commentId = e.currentTarget.dataset.comment_id;

      // Defer layout read to next frame
      requestAnimationFrame(() => {
        const commentElement = document.getElementById(`comment${commentId}`);
        if (commentElement) {
          const commentContent = commentElement.textContent;

          // Batch DOM writes
          commentText.value = commentContent;
          submitButton.textContent = "Update";
          commentForm.action = `edit_comment/${commentId}`;
        }
      });
    });
  }

  // Delete functionality
  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      const { commentId, postSlug } = e.currentTarget.dataset;

      if (commentId && postSlug) {
        // Batch DOM writes
        deleteConfirm.href = `/post/${postSlug}/comment/${commentId}/delete/`;
        deleteModal.show();
      } else {
        console.error("Missing commentId or postSlug on delete button");
      }
    });
  }
});
