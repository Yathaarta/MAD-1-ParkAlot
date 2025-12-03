document.addEventListener('DOMContentLoaded', function() {
    function showDetails(spotId) { 
        const panel = document.getElementById("details-content");
        panel.innerHTML = `<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2 text-muted">Loading details...</p></div>`;

        fetch(`/admin/spot-details/${spotId}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => { throw new Error(errData.error || 'Failed to fetch details'); });
                }
                return response.json();
            })
            .then(data => {
                let htmlContent = '';

                // --- display current status and details ---
                if (data.current_occupied && data.current_booking_details) {
                    // scenario: spot is currently physically occupied
                    htmlContent += `
                        <div class="alert alert-danger mb-3 py-2"><h6 class="mb-0 text-center">Currently Occupied</h6></div>
                        <div class="text-start small">
                            <p class="mb-1"><strong>User:</strong> ${data.current_booking_details.user_name}</p>
                            <p class="mb-1"><strong>Email:</strong> ${data.current_booking_details.email}</p>
                            <p class="mb-1"><strong>Vehicle:</strong> ${data.current_booking_details.vehicle_no}</p>
                            <p class="mb-1"><strong>Start:</strong> ${data.current_booking_details.parking_time}</p>
                            <p class="mb-1"><strong>Expiry:</strong> ${data.current_booking_details.leaving_time}</p>
                            <p class="mb-1"><strong>Cost:</strong> ₹${data.current_booking_details.parking_cost}</p>
                        </div>
                        <hr>
                    `;
                } else if (data.spot_status === 'O' && !data.current_occupied) {
                    htmlContent += `<div class="alert alert-warning text-center small">Spot marked occupied, but no active booking found.</div><hr>`;
                } else {
                    htmlContent += `<div class="alert alert-success text-center py-2"><h6 class="mb-0">Available</h6></div>`;
                    if (data.future_bookings_details.length > 0) {
                        htmlContent += `<p class="text-center text-muted small mb-2">(Booked for future)</p>`;
                    }
                    htmlContent += `<hr>`;
                }

                // --- display future bookings if available ---
                if (data.future_bookings_details && data.future_bookings_details.length > 0) {
                    htmlContent += `
                        <h6 class="text-center mt-3 mb-2">Upcoming Bookings</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-striped table-bordered text-start" style="font-size: 0.85rem;">
                                <thead class="table-light">
                                    <tr>
                                        <th>User</th>
                                        <th>Vehicle</th>
                                        <th>From</th>
                                        <th>Until</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.future_bookings_details.map(fb => `
                                        <tr>
                                            <td>${fb.user_name}</td>
                                            <td>${fb.vehicle_no}</td>
                                            <td>${fb.parking_time.split(' ')[0]}<br><small>${fb.parking_time.split(' ')[1]}</small></td>
                                            <td>${fb.leaving_time.split(' ')[0]}<br><small>${fb.leaving_time.split(' ')[1]}</small></td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else if (!data.current_occupied) {
                    htmlContent += `<p class="text-center text-muted small">No upcoming bookings.</p>`;
                }

                // --- add delete button ---
                htmlContent += `<div class="d-grid gap-2 mt-3">`;
                
                if (data.is_deletable) { 
                    htmlContent += `<button class="btn btn-danger btn-sm" onclick="deleteSpot(${spotId})">Delete Spot</button>`;
                } else {
                    htmlContent += `<div class="text-center text-muted small fst-italic mb-2">Cannot delete (Active/Future bookings)</div>`;
                }
                
                htmlContent += `<button class="btn btn-secondary btn-sm" onclick="clearDetails()">Close</button></div>`;

                panel.innerHTML = htmlContent;

            })
            .catch(error => {
                console.error('Error fetching spot details:', error);
                panel.innerHTML = `<div class="alert alert-danger">Error: ${error.message || 'Could not load details.'}</div>`;
            });
    }

    function clearDetails() {
        document.getElementById("details-content").innerHTML = `<p class="text-center text-muted mt-5">Click a parking spot to view details here.</p>`;
    }
    
    function deleteSpot(spotId) {
        if (confirm('Are you sure you want to delete this spot?')) {
            fetch(`/admin/delete_spot/${spotId}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        location.reload(); 
                    } else {
                        response.json().then(data => {
                            alert(data.error || 'Failed to delete spot.'); 
                        }).catch(() => { 
                            alert('Failed to delete spot. Server error.');
                        });
                    }
                })
                .catch(error => {
                    console.error('Error deleting spot:', error);
                    alert('An error occurred while trying to delete the spot.');
                });
        }
    }

    window.showDetails = showDetails;
    window.clearDetails = clearDetails;
    window.deleteSpot = deleteSpot;
});