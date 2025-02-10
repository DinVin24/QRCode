import src.tools.reed_solomon as rs
import src.tools.version_check as vc
import src.tools.QRdrawer as qd

def final_qr_gen(input_text, ECL):
    ver,size = vc.version_check(input_text,ECL)
    msg = rs.final_codewords(input_text,ECL)

    poza = qd.return_mat(ver,msg,ECL)

    return poza
