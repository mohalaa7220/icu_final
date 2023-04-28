from django.urls import path
from .views import (MedicinesView, MedicineDetails, AddMedicineAllNurses, AddMedicineNurse, GetMedicineUser,
                    GetMedicineNurse, GetPatientDoctorMedicines, GetPatientNurseMedicines, CheckMedicine)

urlpatterns = [

    path('check_medicine', CheckMedicine.as_view(), name='mark_medicine'),

    # Medicine
    path('add_medicine', AddMedicineNurse.as_view(), name='medicine_user'),

    path('add_medicine_all_nurses',
         AddMedicineAllNurses.as_view(), name='medicine_nurses'),

    path('medicines/', GetMedicineUser.as_view(), name='medicines_user'),

    path('medicines/<str:pk>', GetMedicineUser.as_view(),
         name='medicines_user_details'),

    path('medicines_nurse', GetMedicineNurse.as_view(), name='medicines_nurse'),

    path('', MedicinesView.as_view(), name='medicines'),
    path('<str:pk>', MedicineDetails.as_view(), name='medicine_detail'),


    # GetPatientDoctorMedicines
    path('doctor_patient_medicine/<str:pk>',
         GetPatientDoctorMedicines.as_view(), name='medicine_detail'),
    path('nurse_patient_medicine/<str:pk>',
         GetPatientNurseMedicines.as_view(), name='medicine_detail'),

]
