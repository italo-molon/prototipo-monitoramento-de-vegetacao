import cv2
import numpy as np
import os

# ==================== CONFIGURAÇÕES ====================
pasta_imagens = "imagens"
nome_arquivo = "serra_mar.jpg"
caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)

img = cv2.imread(caminho_imagem)
if img is None:
    print("ERRO: Imagem não encontrada!")
    exit()

print(f"Imagem carregada → Dimensões: {img.shape}")

img_suave = cv2.GaussianBlur(img, (3, 3), 0)
hsv = cv2.cvtColor(img_suave, cv2.COLOR_BGR2HSV)
verde_baixo = np.array([10, 45, 50])
verde_alto  = np.array([95, 255, 255])
mask = cv2.inRange(hsv, verde_baixo, verde_alto)

kernel = np.ones((5,5), np.uint8)
mask_limpa = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
mask_limpa = cv2.morphologyEx(mask_limpa, cv2.MORPH_OPEN, kernel, iterations=1)

# Zona de risco
gray = cv2.cvtColor(img_suave, cv2.COLOR_BGR2GRAY)
bordas = cv2.Canny(gray, 30, 100)
zona_risco_bin = cv2.dilate(bordas, np.ones((5,5), np.uint8), iterations=5)
zona_risco = zona_risco_bin.astype(np.uint8)

mask_zona_verde = cv2.bitwise_and(mask_limpa, mask_limpa, mask=zona_risco)

# ==================== INPUT CLIMA + FALHA TÉRMICA AGRESSIVA ====================
print("\nDigite o clima atual (seco / chuvoso / quente): ")
clima = input().strip().lower()

if clima == "chuvoso":
    fator_clima = 1.45
    print("☔ SIMULANDO FALHA TERMICA MUITO AGRESSIVA (chuva forte)...")
    
    # === FALHA TÉRMICA MUITO MAIS FORTE ===
    img_falha = cv2.GaussianBlur(img, (21, 21), 0)           # blur bem forte
    noise = np.random.normal(0, 55, img.shape).astype(np.uint8)  # ruído pesado
    img_falha = cv2.add(img_falha, noise)
    img_falha = cv2.convertScaleAbs(img_falha, alpha=0.45, beta=40)  # contraste bem baixo
    img_falha = cv2.GaussianBlur(img_falha, (9, 9), 0)       # blur extra final
    
else:
    fator_clima = 1.0 if clima == "seco" else 1.25
    img_falha = img.copy()

print(f"Fator climático: {fator_clima}x")

# ==================== FATOR ESPÉCIE ====================
verde_medio = np.mean(hsv[:,:,1][mask_limpa > 0]) if np.any(mask_limpa > 0) else 100
fator_especie = 0.8 if verde_medio < 100 else 1.3
print(f"Fator espécie: {fator_especie}x")

# ==================== PROJEÇÃO ====================
kernel_6  = np.ones((int(7  * fator_clima * fator_especie), int(7  * fator_clima * fator_especie)), np.uint8)
kernel_12 = np.ones((int(13 * fator_clima * fator_especie), int(13 * fator_clima * fator_especie)), np.uint8)

proj_6  = cv2.dilate(mask_zona_verde, kernel_6,  iterations=1)
proj_12 = cv2.dilate(mask_zona_verde, kernel_12, iterations=1)

area_zona = cv2.countNonZero(zona_risco)
perc_hoje = (cv2.countNonZero(mask_zona_verde) / area_zona) * 100 if area_zona > 0 else 0
perc_6    = (cv2.countNonZero(proj_6)  / area_zona) * 100 if area_zona > 0 else 0
perc_12   = (cv2.countNonZero(proj_12) / area_zona) * 100 if area_zona > 0 else 0

print(f"\n📊 RISCO NA ZONA CRÍTICA:")
print(f"   Hoje           → {perc_hoje:.1f}%")
print(f"   +6 meses       → {perc_6:.1f}%")
print(f"   +12 meses      → {perc_12:.1f}%")

podar_50 = cv2.erode(mask_zona_verde, np.ones((9,9), np.uint8), iterations=1)
perc_podado = (cv2.countNonZero(podar_50) / area_zona) * 100 if area_zona > 0 else 0
print(f"   Se podar 50% agora → {perc_podado:.1f}%")

# ==================== SALVAR ====================
cv2.imwrite("01_original.jpg", img)
cv2.imwrite("02_mascara_limpa.jpg", mask_limpa)
cv2.imwrite("03_zona_risco.jpg", zona_risco)
cv2.imwrite("04_proj_6meses.jpg", proj_6)
cv2.imwrite("05_proj_12meses.jpg", proj_12)
cv2.imwrite("06_podado.jpg", podar_50)

if clima == "chuvoso":
    cv2.imwrite("07_falha_termica_chuva_AGRESSIVA.jpg", img_falha)

# ==================== MOSTRAR JANELAS ====================
cv2.imshow('01 - Original', img)
cv2.imshow('02 - Mascara Limpa', mask_limpa)
cv2.imshow('03 - Zona de Risco', zona_risco)
cv2.imshow('04 - Projecao +6 meses', proj_6)
cv2.imshow('05 - Projecao +12 meses', proj_12)
cv2.imshow('06 - Simulacao Podada', podar_50)

if clima == "chuvoso":
    cv2.imshow('07 - Falha Térmica AGRESSIVA (chuva)', img_falha)

print("\nJanelas abertas! Pressione qualquer tecla para fechar...")
cv2.waitKey(0)
cv2.destroyAllWindows()