
document.addEventListener("DOMContentLoaded", function () {

    // MAP
    const mapElement = document.getElementById("vallacar-map");

    if (mapElement && typeof L !== "undefined") {

        const map = L.map("vallacar-map").setView(
            [10.6765, 122.9509],
            7
        );

        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors"
            }
        ).addTo(map);

        const locations = [
            {
                name: "Bacolod",
                coordinates: [10.6765, 122.9509]
            },
            {
                name: "Iloilo",
                coordinates: [10.7202, 122.5621]
            },
            {
                name: "Cebu",
                coordinates: [10.3157, 123.8854]
            }
        ];

        locations.forEach(function (location) {
            L.marker(location.coordinates)
                .addTo(map)
                .bindPopup("<b>" + location.name + "</b>");
        });

        L.polyline(
            locations.slice(0, 2).map(
                location => location.coordinates
            ),
            {
                color: "#397cf6",
                weight: 4,
                opacity: 0.8
            }
        ).addTo(map);

        setTimeout(function () {
            map.invalidateSize();
        }, 300);
    }


    // DATABASE CHART DATA
    const chartElement = document.getElementById("chart-data");

    if (chartElement && typeof Chart !== "undefined") {

        let data = {
            delivered: 0,
            transit: 0,
            pending: 0,
            cancelled: 0
        };

        try {
            data = JSON.parse(chartElement.textContent);
        } catch (error) {
            console.error("Chart data could not be loaded:", error);
        }

        const canvas = document.getElementById("shipmentChart");

        if (canvas) {
            new Chart(canvas, {
                type: "doughnut",

                data: {
                    labels: [
                        "Delivered",
                        "In Transit",
                        "Pending",
                        "Cancelled"
                    ],

                    datasets: [{
                        data: [
                            data.delivered || 0,
                            data.transit || 0,
                            data.pending || 0,
                            data.cancelled || 0
                        ],

                        backgroundColor: [
                            "#22bd91",
                            "#397cf6",
                            "#e5a03e",
                            "#ed5192"
                        ],

                        borderWidth: 0,
                        hoverOffset: 7
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    cutout: "72%",

                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }


    // SEARCH RECENT SHIPMENTS
    const search = document.getElementById("globalSearch");

    if (search) {
        search.addEventListener("input", function () {

            const value = this.value.toLowerCase();

            document.querySelectorAll(".recent-panel tbody tr")
                .forEach(function (row) {

                    row.style.display = row.textContent
                        .toLowerCase()
                        .includes(value) ? "" : "none";

                });
        });
    }

});
