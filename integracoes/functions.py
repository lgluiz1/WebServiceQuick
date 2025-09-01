import requests
import urllib3
from datetime import datetime
from django.core.mail import send_mail as django_send_mail

# Suprimir aviso de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def envia_para_senac_soap(dado):
    url = "https://www.editorasenacsp.com.br/ms/sapiens_Asyncbr_senac_sp_eds_ven_confirmacaoentrega"

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "user_key": "176fb9e18053f63bfe350017192340e8",
        "SOAPAction": "http://services.senior.com.br/dadosEntrega",
        "User-Agent": "Mozilla/5.0",
    }

    # 📅 Converte a data para dd/MM/yyyy HH:mm:ss
    data_entrega = dado.get("ice_f_e_fit_fte_finisher_occurrence_at")
    if data_entrega:
        try:
            dt = datetime.fromisoformat(data_entrega.replace("Z", "").split(".")[0])
            data_entrega = dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            data_entrega = "01/01/1900 00:00:00"
    else:
        data_entrega = "01/01/1900 00:00:00"

    # 🔢 Corrige valores numéricos
    peso = str(dado.get("ice_f_e_ioe_weight", "0")).replace(".", ",")
    valor = str(dado.get("ice_f_e_ioe_value", "0")).replace(".", ",")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.senior.com.br">
       <soapenv:Header/>
       <soapenv:Body>
          <ser:dadosEntrega>
             <user>sapienssid</user>
             <password>jcmm@@</password>
             <encryption>0</encryption>
             <parameters>
                <cargas>
                   <cepEnt>{dado.get('ice_f_e_ioe_rpt_mds_postal_code','00000000')}</cepEnt>
                   <ctoNfs>{dado.get('ice_f_e_ioe_number','00')}</ctoNfs>
                   <nomCid>{dado.get('ice_f_e_ioe_rpt_mds_cty_name','Cidade')}</nomCid>
                   <nomDes>{dado.get('ice_f_e_ioe_rpt_name','Destinatario')}</nomDes>
                   <numNfs>{dado.get('ice_f_e_ioe_number','00')}</numNfs>
                   <pesCkg>{peso}</pesCkg>
                   <pesRkg>{peso}</pesRkg>
                   <qtdVol>{dado.get('ice_f_e_ioe_volume',0)}</qtdVol>
                   <sigUfs>{dado.get('ice_f_e_fit_rpt_mds_cty_sae_code','XX')}</sigUfs>
                   <tipFre>C</tipFre>
                   <vlrCrg>{valor}</vlrCrg>
                   <vlrDst>0,00</vlrDst>
                   <vlrFre>0,00</vlrFre>
                   <vlrLiq>{valor}</vlrLiq>
                </cargas>
                <cnpjTr>08296144000149</cnpjTr>
                <datEnt>{data_entrega}</datEnt>
                <flowInstanceID></flowInstanceID>
                <flowName></flowName>
             </parameters>
          </ser:dadosEntrega>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    try:
        response = requests.post(url, data=xml.encode("utf-8"), headers=headers, verify=False, timeout=60)
        return response.status_code, response.text
    except Exception as e:
        return 500, f"Erro de conexão: {str(e)}"



def enviar_email(assunto, resultado):    
    django_send_mail(
        subject=assunto,
        message=resultado,
        from_email='naorespondertest@gmail.com',
        recipient_list=['legalhints@gmail.com'],
        fail_silently=False,
    )

    return (200, "Email enviado com sucesso")

