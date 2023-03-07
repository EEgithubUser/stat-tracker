function deleteStatsnapshot(statsnapshotId) {
  fetch("/delete-statsnapshot", {
    method: "POST",
    body: JSON.stringify({ statsnapshotId: statsnapshotId }),
  }).then((_res) => {
    window.location.href = "/statbook";
  });
}
