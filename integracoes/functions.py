import requests
import urllib3

# Suprimir aviso de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def envia_para_senac_soap(dado):

    url = "https://www.editorasenacsp.com.br/ms/sapiens_Asyncbr_senac_sp_eds_ven_confirmacaoentrega"

    # Monta o XML dinamicamente com os dados do payload
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
                   <pesCkg>{dado.get('ice_f_e_ioe_weight','0,000')}</pesCkg>
                   <pesRkg>{dado.get('ice_f_e_ioe_weight','0,000')}</pesRkg>
                   <qtdVol>{dado.get('ice_f_e_ioe_volume',0)}</qtdVol>
                   <sigUfs>{dado.get('ice_f_e_fit_rpt_mds_cty_sae_code','XX')}</sigUfs>
                   <tipFre>C</tipFre>
                   <vlrCrg>{dado.get('ice_f_e_ioe_value','0,00')}</vlrCrg>
                   <vlrDst>0,00</vlrDst>
                   <vlrFre>0,00</vlrFre>
                   <vlrLiq>{dado.get('ice_f_e_ioe_value','0,00')}</vlrLiq>
                </cargas>
                <cnpjTr>{dado.get('ice_f_e_fit_crn_psn_document','00000000000000')}</cnpjTr>
                <datEnt>{dado.get('ice_f_e_fit_fte_finisher_occurrence_at','01/01/1900')}</datEnt>
                <flowInstanceID></flowInstanceID>
                <flowName></flowName>
             </parameters>
          </ser:dadosEntrega>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "user_key": "176fb9e18053f63bfe350017192340e8",
        "SOAPAction": "",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, data=xml.encode("utf-8"), headers=headers, verify=False)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    return response.status_code, response.text
