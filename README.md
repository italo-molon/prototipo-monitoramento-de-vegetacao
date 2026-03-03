# Protótipo de Monitoramento de Vegetação Próximas a Torres de Transmissão (Circuito Simples / Circuito Duplo)

Protótipo desenvolvido por Ítalo Molon (Estudante do 3º Semestre do Curso de Inteligência Artificial)

## O que faz
- Detecta vegetação em imagens de drone usando OpenCV (HSV + morfologia).
- Cria zona de risco ao redor de cabos/torres.
- Simula crescimento futuro (6 e 12 meses) com fatores climáticos (seco, quente, chuvoso) e espécie.
- Inclui simulação agressiva de falha térmica em chuva (complemento aos drones térmicos da ISA).

## Resultados por clima (exemplo)
| Clima     | Hoje   | +6 meses | +12 meses | Se podar 50% agora |
|-----------|--------|----------|-----------|--------------------|
| Seco      | 76.1%  | 81.0%    | 84.7%     | 65.3%              |
| Quente    | 76.1%  | 82.9%    | 86.1%     | 65.3%              |
| Chuvoso   | 76.1%  | 83.5%    | 86.7%     | 65.3%              |

## Tecnologias
- Python + OpenCV
- Filtragem HSV
- Morfologia (dilatação/erosão)
- Simulação simples de fatores ambientais

## Próximos passos
- Integração com dados reais de drones térmicos
- Processamento em batch de múltiplas imagens
- Dashboard simples (ex: Streamlit)

Relatório completo (PDF): https://github.com/italo-molon/prototipo-monitoramento-de-vegetacao/blob/main/Monitoramento%20de%20Vegeta%C3%A7%C3%A3o.pdf

Contato:  
LinkedIn: https://www.linkedin.com/in/italomolontech/  
E-mail: italo.prog@gmail.com / italo.molon7@gmail.com
