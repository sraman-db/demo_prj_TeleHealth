// Dummy doctor data - 20 doctors from Bhubaneswar
const doctors = [
    {
        name: "Dr. Rajesh Kumar Panda",
        department: "Cardiology",
        qualification: "MBBS, MD, DM (Cardiology)",
        address: "Apollo Hospitals, Sainik School Road, Bhubaneswar - 751005",
        photo: "https://ui-avatars.com/api/?name=Rajesh+Panda&background=667eea&color=fff&size=200"
    },
    {
        name: "Dr. Sneha Mohanty",
        department: "Pediatrics",
        qualification: "MBBS, MD (Pediatrics)",
        address: "KIMS Hospital, Patia, Bhubaneswar - 751024",
        photo: "https://ui-avatars.com/api/?name=Sneha+Mohanty&background=764ba2&color=fff&size=200"
    },
    {
        name: "Dr. Amit Kumar Sahoo",
        department: "Orthopedics",
        qualification: "MBBS, MS (Orthopedics)",
        address: "Care Hospital, Nayapalli, Bhubaneswar - 751012",
        photo: "https://ui-avatars.com/api/?name=Amit+Sahoo&background=f093fb&color=fff&size=200"
    },
    {
        name: "Dr. Priyanka Das",
        department: "Gynecology",
        qualification: "MBBS, MD (Obstetrics & Gynecology)",
        address: "Sun Hospital, Jayadev Vihar, Bhubaneswar - 751013",
        photo: "https://ui-avatars.com/api/?name=Priyanka+Das&background=4facfe&color=fff&size=200"
    },
    {
        name: "Dr. Subash Chandra Jena",
        department: "Neurology",
        qualification: "MBBS, MD, DM (Neurology)",
        address: "Kalinga Hospital, Chandrasekharpur, Bhubaneswar - 751016",
        photo: "https://ui-avatars.com/api/?name=Subash+Jena&background=00f2fe&color=fff&size=200"
    },
    {
        name: "Dr. Anita Pattnaik",
        department: "Dermatology",
        qualification: "MBBS, MD (Dermatology)",
        address: "Hi-Tech Medical College, Rourkela Road, Bhubaneswar - 751025",
        photo: "https://ui-avatars.com/api/?name=Anita+Pattnaik&background=43e97b&color=fff&size=200"
    },
    {
        name: "Dr. Bikash Ranjan Mishra",
        department: "General Surgery",
        qualification: "MBBS, MS (General Surgery)",
        address: "Capital Hospital, Unit-6, Bhubaneswar - 751001",
        photo: "https://ui-avatars.com/api/?name=Bikash+Mishra&background=fa709a&color=fff&size=200"
    },
    {
        name: "Dr. Mamta Swain",
        department: "Ophthalmology",
        qualification: "MBBS, MS (Ophthalmology)",
        address: "LV Prasad Eye Institute, Patia, Bhubaneswar - 751024",
        photo: "https://ui-avatars.com/api/?name=Mamta+Swain&background=fee140&color=333&size=200"
    },
    {
        name: "Dr. Prasanta Kumar Dash",
        department: "ENT",
        qualification: "MBBS, MS (ENT)",
        address: "Sum Hospital, Kalinga Nagar, Bhubaneswar - 751003",
        photo: "https://ui-avatars.com/api/?name=Prasanta+Dash&background=30cfd0&color=fff&size=200"
    },
    {
        name: "Dr. Swati Behera",
        department: "Psychiatry",
        qualification: "MBBS, MD (Psychiatry)",
        address: "Manipal Hospital, Kharavel Nagar, Bhubaneswar - 751001",
        photo: "https://ui-avatars.com/api/?name=Swati+Behera&background=a8edea&color=333&size=200"
    },
    {
        name: "Dr. Santosh Kumar Nayak",
        department: "Nephrology",
        qualification: "MBBS, MD, DM (Nephrology)",
        address: "Apollo Hospitals, Sainik School Road, Bhubaneswar - 751005",
        photo: "https://ui-avatars.com/api/?name=Santosh+Nayak&background=fed6e3&color=333&size=200"
    },
    {
        name: "Dr. Rashmi Ranjan Patra",
        department: "Gastroenterology",
        qualification: "MBBS, MD, DM (Gastroenterology)",
        address: "AMRI Hospital, Khandagiri, Bhubaneswar - 751030",
        photo: "https://ui-avatars.com/api/?name=Rashmi+Patra&background=c471f5&color=fff&size=200"
    },
    {
        name: "Dr. Lipsa Pradhan",
        department: "Pulmonology",
        qualification: "MBBS, MD (Pulmonology)",
        address: "KIMS Hospital, Patia, Bhubaneswar - 751024",
        photo: "https://ui-avatars.com/api/?name=Lipsa+Pradhan&background=fa7e1e&color=fff&size=200"
    },
    {
        name: "Dr. Debasis Routray",
        department: "Urology",
        qualification: "MBBS, MS, MCh (Urology)",
        address: "Care Hospital, Nayapalli, Bhubaneswar - 751012",
        photo: "https://ui-avatars.com/api/?name=Debasis+Routray&background=d76d77&color=fff&size=200"
    },
    {
        name: "Dr. Suchitra Mohapatra",
        department: "Radiology",
        qualification: "MBBS, MD (Radiology)",
        address: "Sun Hospital, Jayadev Vihar, Bhubaneswar - 751013",
        photo: "https://ui-avatars.com/api/?name=Suchitra+Mohapatra&background=3eecac&color=fff&size=200"
    },
    {
        name: "Dr. Alok Kumar Rout",
        department: "Oncology",
        qualification: "MBBS, MD, DM (Medical Oncology)",
        address: "Kalinga Hospital, Chandrasekharpur, Bhubaneswar - 751016",
        photo: "https://ui-avatars.com/api/?name=Alok+Rout&background=ee9ae5&color=fff&size=200"
    },
    {
        name: "Dr. Madhuri Parida",
        department: "Endocrinology",
        qualification: "MBBS, MD, DM (Endocrinology)",
        address: "Hi-Tech Medical College, Rourkela Road, Bhubaneswar - 751025",
        photo: "https://ui-avatars.com/api/?name=Madhuri+Parida&background=5ee7df&color=fff&size=200"
    },
    {
        name: "Dr. Biswajit Senapati",
        department: "Rheumatology",
        qualification: "MBBS, MD, DM (Rheumatology)",
        address: "Capital Hospital, Unit-6, Bhubaneswar - 751001",
        photo: "https://ui-avatars.com/api/?name=Biswajit+Senapati&background=b490ca&color=fff&size=200"
    },
    {
        name: "Dr. Namita Sahu",
        department: "Anesthesiology",
        qualification: "MBBS, MD (Anesthesiology)",
        address: "Sum Hospital, Kalinga Nagar, Bhubaneswar - 751003",
        photo: "https://ui-avatars.com/api/?name=Namita+Sahu&background=f6d365&color=333&size=200"
    },
    {
        name: "Dr. Ramesh Chandra Behera",
        department: "General Medicine",
        qualification: "MBBS, MD (General Medicine)",
        address: "Manipal Hospital, Kharavel Nagar, Bhubaneswar - 751001",
        photo: "https://ui-avatars.com/api/?name=Ramesh+Behera&background=fda085&color=fff&size=200"
    }
];

// Store all doctors and filtered doctors
let allDoctors = [...doctors];
let filteredDoctors = [...doctors];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    displayDoctors(allDoctors);
    setupSearch();
});

// Display doctors in grid
function displayDoctors(doctorsToDisplay) {
    const grid = document.getElementById('doctorsGrid');
    const noResults = document.getElementById('noResults');
    
    if (doctorsToDisplay.length === 0) {
        grid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    noResults.style.display = 'none';
    grid.innerHTML = '';
    
    doctorsToDisplay.forEach(doctor => {
        const card = createDoctorCard(doctor);
        grid.appendChild(card);
    });
}

// Create doctor card element
function createDoctorCard(doctor) {
    const card = document.createElement('div');
    card.className = 'doctor-card';
    
    card.innerHTML = `
        <div class="doctor-header">
            <img src="${doctor.photo}" alt="${doctor.name}" class="doctor-photo" />
            <div class="doctor-title">
                <h2 class="doctor-name">${doctor.name}</h2>
                <p class="doctor-department">${doctor.department}</p>
            </div>
        </div>
        
        <div class="doctor-details">
            <div class="detail-item">
                <i class="ri-award-line"></i>
                <div class="detail-content">
                    <div class="detail-label">Qualification</div>
                    <div class="detail-text">${doctor.qualification}</div>
                </div>
            </div>
            
            <div class="detail-item">
                <i class="ri-hospital-line"></i>
                <div class="detail-content">
                    <div class="detail-label">Clinic Address</div>
                    <div class="detail-text">${doctor.address}</div>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Setup search functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            filteredDoctors = [...allDoctors];
        } else {
            filteredDoctors = allDoctors.filter(doctor => {
                return (
                    doctor.name.toLowerCase().includes(searchTerm) ||
                    doctor.department.toLowerCase().includes(searchTerm) ||
                    doctor.qualification.toLowerCase().includes(searchTerm) ||
                    doctor.address.toLowerCase().includes(searchTerm)
                );
            });
        }
        
        displayDoctors(filteredDoctors);
    });
}