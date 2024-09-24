frappe.pages['gps-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'GPS Dashboard',
        single_column: true
    });

    // Load the HTML content
    $(frappe.render_template('gps_dashboard')).appendTo(page.body);

    // Initialize the map
    var map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var markers = L.layerGroup().addTo(map);

    // Function to load and display markers
    function loadMarkers(entityType) {
        frappe.call({
            method: 'church.church.page.gps_dashboard.gps_dashboard.get_gps_data',
            args: {
                entity_type: entityType
            },
            callback: function(r) {
                markers.clearLayers();
                if (r.message) {
                    r.message.forEach(function(entity) {
                        var marker = L.marker([entity.latitude, entity.longitude])
                            .addTo(markers)
                            .bindPopup(entity.name);

                        marker.on('click', function() {
                            showEntityDetails(entity);
                        });
                    });
                    
                    // Fit the map to the markers
                    var group = new L.featureGroup(markers.getLayers());
                    map.fitBounds(group.getBounds());
                }
            }
        });
    }

    // Function to show entity details
    function showEntityDetails(entity) {
        var detailsHtml = `
            <h4>${entity.name}</h4>
            <p><strong>Type:</strong> ${entity.entity_type}</p>
            <p><strong>Total Contributions:</strong> ${entity.total_contributions}</p>
        `;
        $('#entity-details').html(detailsHtml);
    }

    // Event listener for entity type selection
    $('#entity-type').on('change', function() {
        loadMarkers($(this).val());
    });

    // Initial load of all markers
    loadMarkers('all');
};