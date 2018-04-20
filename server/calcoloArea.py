from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert, butter, lfilter, freqz
from utils import mhs, hilb, interp
from EMD_main import EMD
import pylab as py



#print(f_or,f_ir,f_b)

# with open("dataset/A.csv","r") as danneggiato:
# 	lettura = danneggiato.read().split("\n")
# 	vibrationDanneggiato=[]
# 	for ind,v in enumerate(lettura):
# 		try:
# 			vibrationDanneggiato.append(v.split(",")[1])
# 		except:
# 			pass
#
# for n, el in enumerate(vibrationDanneggiato):
# 	vibrationDanneggiato[n-1] = float(el)

def calcoloFeatures(lista_float):
	nb = 6
	fr = 200/60.0
	db = 1
	dp = 6.5
	alfa = 0

	f_or = nb/2  * fr * (1 - db/dp * np.cos(alfa))
	f_ir = nb/2  * fr * (1 + db/dp * np.cos(alfa))
	f_b  = dp/db * fr * (1 - (db/dp * np.cos(alfa))**2)

	lista_float = np.array(lista_float, np.float32)
	timeLine = np.linspace(0, len(lista_float), len(lista_float))


	# EMD #
	emd = EMD()
	emd.FIXE_H = 3
	emd.nbsym = 2
	emd.splineKind = 'cubic'

	fcamp=1/len(lista_float)
	timeLine = t = np.linspace(0, len(lista_float), len(lista_float))
	VibrationNump = np.array(lista_float, np.float32)
	IMF, EXT, ITER, imfNo = emd.emd(VibrationNump, timeLine, -1)

	c = np.floor(np.sqrt(imfNo + 3))
	r = np.ceil((imfNo + 2) / c)

	def butter_lowpass(cutoff, fs, order=5):
		nyq = 0.5*fs
		normal_cutoff = cutoff / nyq
		b, a = butter(order, normal_cutoff, btype='low', analog=False)
		return b,a

	def butter_lowpass_filter(data, cutoff, fs, order=5):
		b, a = butter_lowpass(cutoff, fs, order=order)
		y = lfilter(b,a,data)
		return y

	mhsf_for = []
	mhsf_fir = []
	mhsf_fb  = []


	for num in range(imfNo):
		H, Amp, phase = hilb(IMF[num], unwrap=True)
		freq = np.diff(phase)/(2 * np.pi) * fcamp
		f, hf = mhs(Amp, freq)

		mhsf = interp(f, hf) #interpolante

		# ABBIAMO CALCOLATO L'MHS PER TUTTI GLI IMF, ORA BISOGNA TROVARE IL VALORE MASSIMO
		# DI TUTTI GLI MHS NELLE 3 FREQUENZE (f_or, f_ir, f_b)
		mhsf_for.append(mhsf(f_or))
		mhsf_fir.append(mhsf(f_ir))
		mhsf_fb.append(mhsf(f_b))

		##trovare il maggiore tra gli mhsf_for, mhsf_fir, mhsf_fb

		#passabasso
		fs = 50 # Hz, sample rate (un valore ogni 0.5s)
		order= 6 ######### ??????????????

		#FOURIER
		DanneggiatoFFT=fft(lista_float)
		PS=np.abs(DanneggiatoFFT)**2
		AREA=np.trapz(PS)
		LP_for=butter_lowpass_filter(lista_float,f_or,fs,order)
		FORFFT=fft(LP_for)
		PSFOR=np.abs(FORFFT)**2
		FOR_AREA=np.trapz(PSFOR)
		FOR_FEAT=FOR_AREA/AREA
		LP_fir=butter_lowpass_filter(lista_float,f_ir,fs,order)
		FIRFFT=fft(LP_fir)
		PSFIR=np.abs(FIRFFT)**2
		FIR_AREA=np.trapz(PSFIR)
		FIR_FEAT=FIR_AREA/AREA
		LP_fb=butter_lowpass_filter(lista_float,f_b,fs,order)
		FBFFT=fft(LP_fb)
		PSFB=np.abs(FBFFT)**2
		FB_AREA=np.trapz(PSFB)
		FB_FEAT=FB_AREA/AREA
		#PLOTTING#
		#plt.subplot(r, c, num + 3)
		#plt.plot(timeLine, IMF[num], 'g')
		#plt.title("IMF no " + str(num))


	max_for = max(mhsf_for)
	max_fir = max(mhsf_fir)
	max_fb  = max(mhsf_fb)
	# print(FOR_FEAT)
	# print(FIR_FEAT)
	# print(FB_FEAT)
	# print(max_for)
	# print(max_fir)
	# print(max_fb)
	return FOR_FEAT,FIR_FEAT,FB_FEAT,max_for,max_fir,max_fb



#calcoloFeatures(vibrationDanneggiato)
