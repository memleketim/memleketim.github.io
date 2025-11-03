document.addEventListener('DOMContentLoaded', () => {
    const draggables = document.querySelectorAll('.draggable');
    const dropAreas = document.querySelectorAll('.drop-area');
    const correctSound = document.getElementById('correctSound');
    const imageSlots = document.querySelectorAll('.image-slot');

    // Doğru eşleşmeler (resim ID -> doğru isim)
    const correctMatches = {
        1: "İznik Kalesi",
        2: "Ayasofya",
        3: "Orhan Camii",
        4: "Süleyman Paşa Medresesi",
        5: "İznik Yeşil Camii",
        6: "İznik Roma Tiyatrosu",
        7: "İznik Gölü",
        8: "Aziz Neophytos Bazilikası"
    };

    let completedCount = 0;

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', () => {
            draggable.classList.add('dragging');
        });

        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
        });
    });

    dropAreas.forEach(area => {
        area.addEventListener('dragover', e => {
            e.preventDefault();
            const dragging = document.querySelector('.dragging');
            if (dragging) {
                area.style.backgroundColor = '#e8f4fd';
            }
        });

        area.addEventListener('dragleave', () => {
            area.style.backgroundColor = '';
        });

        area.addEventListener('drop', e => {
            e.preventDefault();
            const dragging = document.querySelector('.dragging');
            if (!dragging) return;

            const targetId = area.dataset.target;
            const correctValue = correctMatches[targetId];
            const droppedValue = dragging.dataset.value;

            if (correctValue === droppedValue) {
                // Doğru eşleşme
                area.textContent = droppedValue;
                area.classList.add('filled');
                dragging.style.display = 'none'; // Etiketi gizle
                completedCount++;

                // Ses çal
                if (correctSound) {
                    correctSound.currentTime = 0;
                    correctSound.play().catch(e => console.log("Ses çalınamadı:", e));
                } else {
                    console.log("Doğru! 🎉");
                }

                // Tüm eşleşmeler tamam mı?
                if (completedCount === Object.keys(correctMatches).length) {
                    setTimeout(() => {
                        showCongrats();
                    }, 500);
                }
            } else {
                // Yanlış eşleşme - etiket eski yerine döner
                alert("Yanlış eşleştirme! Tekrar deneyin.");
            }

            area.style.backgroundColor = '';
        });
    });

    function showCongrats() {
        const congrats = document.createElement('div');
        congrats.id = 'congrats';
        congrats.innerHTML = `
            <h2>🎉 Tebrikler! 🎉</h2>
            <p>Tüm eşleştirmeleri doğru yaptınız!</p>
            <button onclick="location.reload()">Yeniden Oyna</button>
        `;
        document.body.appendChild(congrats);
        congrats.style.display = 'flex';
    }
});