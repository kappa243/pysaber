import numpy as np

from pysaber.api import CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES
from pysaber.saber_indcpa import indcpa_kem_keypair, indcpa_kem_enc, indcpa_kem_dec
from pysaber.saber_params import (SABER_INDCPA_PUBLICKEYBYTES,
                                  SABER_INDCPA_SECRETKEYBYTES, SABER_BYTES_CCA_DEC)
from tests.common import rng_init
from pysaber.pack_unpack import POLVECp2BS, POLVECq2BS, BS2POLVECp, BS2POLmsg, POLT2BS, BS2POLT, POLmsg2BS

def test_indcpa_kem_keypair():

    rng_init()

    pk = np.zeros(CRYPTO_PUBLICKEYBYTES, dtype=np.uint8)
    sk = np.zeros(CRYPTO_SECRETKEYBYTES, dtype=np.uint8)

    indcpa_kem_keypair(pk, sk)

    result_pk = ""
    for i in range(SABER_INDCPA_PUBLICKEYBYTES):
        result_pk += f"{pk[i]:02x}"

    result_sk = ""
    for i in range(SABER_INDCPA_SECRETKEYBYTES):
        result_sk += f"{sk[i]:02x}"

    assert (
        result_pk
        == "ebaea9177ab60cdb21e5b6df969f19af73071fa3050b4ca8907e9bfe385ae7e4e9f1b64abf3b0683619d1246d3a724ce2c93c4b57762d85947bea2896942e8aa1e7bb2f3ffba51a296d97f9133c3a8c74dfd18e38de5b5240e41e8859168058424c65cdf9cd1905202f88a5af7721f85064174f2f927b97d6981ce5f261fa21ffabe74bb3b79b323a54822a705a6a68157c2eed1f37a9f5c69a1d5a667c1ba35d4bf6ff1d21f37bb090e9355ddee4b3a87a8cce838a1b0a7f6a747514b48b20898d364afcca132dc0f52fb12073c235d281f7b03341b0a1b0ba6ee64dcd6d641383d82471e882a6a959f8ea8427557a5a3f0ee6505f0d4d52c99051fb6fec2a94e7361836726b8a927f458a89d18d0589f9ec2fb2819e1576f9772ec0b628c29e87dfc35eda26aba1dd566a9ca6dba05519ccdcf6409225b1876153f43ca0b2def9697a5a53a449b46e1eaa7bc3f054e5da83ab68c086ea0c9a98c322965e9b4466d52c61b83c62345eea28be14cb5c96f45471ef7ef6076afe3df3fa7a88899c62e32bfdcbfdf8897644513808c10a209bffa38f7ea94e6ac0f139bc3b8adffc4af36745630be3da75038777e979cfec0c4bd19470e1cdc2f2986dcb242fb707f56332e753b0db98e68c1089787c2f1dbb33f8e021c5289d6440d6561274fe6ff148601bfc9393a1a50a9df1a11a27447806bf04912e9c2103c35e7ba8ec94332b4daaea0d79f9a21ad7e450957b1468d3ba44777e65e4f34b41080ce900d3bcb46eb6971a25146bd5ba91d0cace1c8303b6210f1bce649ccfd92ed1061ce8a468fe689c8e5dee28c2d5cf71a88c1b3fd4282039b97290de923dc5a02e0ce1c6f6eaf54504b227a44183c194a799cf570fb017d6a52bb88dff862c0fdb317dfdb5b3a4c579a9900234705a0cd878a6a23f1e9064bcb158e92d7e468755f3ce96d2cd9240e93e96befc67342236f4bb7fe5435a592f0956df270d989c21c09635ec65ac9b2fb42adabd6a489e3a8adfbf13bc55e967e72baa5cdcc8504f5ad5ee180ccff568f0cbccf3302fed290db4511ad811269cf41ec9cae0e5b92b154f1c6d5d2384df629cfaa00dac0547e2fd37cfee3dad7d5a033f637cccdae534de009e6922a3d87d61776664652885ca55eb39aabbbabec66a9cd71822d485f3dc0a0f6dd685925bf2634e48853c22cc07cb11a3f5eb93d07dbb98497633401e8ea1607b03f0c77d803ef7e61fd221fc0b23a853624d92f95d6065e78b2ec47ac9023c1dcc06b27c99e6049b5fe67f64b9130e741765c18ada9bef7296f4aeb5c745e194ca92dbbd602f0f436c60cf1e8e62d01f95ecd9fcba04f6f3cb5c1bf7e39078800a7a766be5e244ad3fce29e39839cfe82c9aaabf27ccf2fc653562d938f"
    )
    assert (
        result_sk
        == "01e0ff030000e0ff0540000000ff3f00008000e0ffffff00f8fffebfffffff0110000400000800024000fc7f000000fe7f000000fe1f00f07f00100000c0ff0700ff3f000000ffdfff0180ffefffffffffff7f00f0ffffbfff0f00000000fcffff0f000240001000002000040001f0ff0100000000012000048001100002c0fffffffd3f00fcff00f0ff0180ff0f00ff3f00f87f00e0fffd7f0000000000000080001000feffff0700010000fcff001000fabfff070003c0ff030001e0ff0140001800002000048000f0fffbbfff0700fe1f000480fffffffd7f000000ff5f00fc7f0040000280ff1f00ff5f00040001300000c0ff070000c0ffff7f00f0ff018000f8ff012000f8ffffdfff0180000000020000088000e0ffffbfff070000e0ff0f00ff0f000080ff0f000120000400000000008000f8ffff3f00008000f0ff0300000800fddfff030000e0ffffffff0700012000fcff0010000480fff7ff01c0ff0b0000e0ff03c0ff0700ffffff0780ffefff0580ff0f000100000080ff0f00feffff0f00022000fc7f00100004c0ff0f000220000480ff0f0000c0ff0f00ff1f00008000f0ff010000080003e0ff07000010000080ff0f00012000f8ffff2f00fe7fff0f00ff3f0000000010000680ffefff0000000080ff0f00fc3f00080000000000000010000400000800fd1f00fc7f01e0fffdbf000800014000080000e0ff010000f0ff0120000400011000024000f0ff0020000880ff2f0004c0ffffffff7f00000000e0ff03000000000020000080000000feffff0700012000fcffff0f00fcbf00f8fffe1f00fc7f0120000000000000000000fc7f000000020000f8ff0000000880001000fe7f000800006000fcff003000feffff1700000000040000f0ff070000f0fffe1f00f87f011000fabf00080001e0ff0300000000fe7f000800fe5f000880ff3f0002000000000220000400ffffff034000000000e0ff0780ffdfff05c0fff7ffffdfff0780fe1f0002800000000120000000001000feffffffff01200000800110000000000000ff1f000880ffefff03c0ff17000040000880001000fa3f000800000000000001000002400010000000000480000000feffff0f00004000f87f02f0fffdfffff7ff00e0ff0b80001000fe3f00f0fffe1f000880ff0f00fcbffff7ff0040000080ffffffff7f0000000260000000ff1f00fabf001000012000fcffffffff01000000000000000480001000fcbfffffff004000f4ff0000000240000800ffffff0780fe2f00fefffff7ffff5f000000ff1f0002c0ff0f00fcffff0700011000000000f8ff010000040000e0ff0340ff0f00010000fc7fff1f00febf00f8fffe1f000800ff0f00fe3f0008000180ff0b80ffefff0340000800010000fcffff0f00febfff0700fe3f000c0000e0ff050000f8ff00e0ff0380ffefff0580ffffffff5f00f87f00d0ffff3f00e8ff012000fcffff0f0000c0fff7fffe3f00f4ff00e0fffdffffffff01e0ff0380000000000000f8ff002000088000f0ff0740000800012000f87f00e0ffff3f00f0fffeffffffffff1f00004000f8ff012000040000f0ff0140000800ff3f00fc7f0110000400000800fe3f000400001000020000f0ff0220000000013000fe7f00000000200004800010000080000000ff3f00f87f011000fe3f00080000c0ffffffffeffffdfffff7ff020000fc7fff0f00fcffff0f00ffffff070000f0fffd7f001000"
    )


def test_indcpa_kem_enc():
    rng_init()

    #input for function under testing
    m_hex = "3BD09B6EA5E37E540373187B7A91F74856573540E753715644B84276FEFF1765"
    seed_sp_hex = "AFB05FB627B9446D5323C4D59D67BE418B1F6C5AF009DD7A53068C6D41F93E8C"
    pk_hex = "EBAEA9177AB60CDB21E5B6DF969F19AF73071FA3050B4CA8907E9BFE385AE7E4E9F1B64ABF3B0683619D1246D3A724CE2C93C4B57762D85947BEA2896942E8AA1E7BB2F3FFBA51A296D97F9133C3A8C74DFD18E38DE5B5240E41E8859168058424C65CDF9CD1905202F88A5AF7721F85064174F2F927B97D6981CE5F261FA21FFABE74BB3B79B323A54822A705A6A68157C2EED1F37A9F5C69A1D5A667C1BA35D4BF6FF1D21F37BB090E9355DDEE4B3A87A8CCE838A1B0A7F6A747514B48B20898D364AFCCA132DC0F52FB12073C235D281F7B03341B0A1B0BA6EE64DCD6D641383D82471E882A6A959F8EA8427557A5A3F0EE6505F0D4D52C99051FB6FEC2A94E7361836726B8A927F458A89D18D0589F9EC2FB2819E1576F9772EC0B628C29E87DFC35EDA26ABA1DD566A9CA6DBA05519CCDCF6409225B1876153F43CA0B2DEF9697A5A53A449B46E1EAA7BC3F054E5DA83AB68C086EA0C9A98C322965E9B4466D52C61B83C62345EEA28BE14CB5C96F45471EF7EF6076AFE3DF3FA7A88899C62E32BFDCBFDF8897644513808C10A209BFFA38F7EA94E6AC0F139BC3B8ADFFC4AF36745630BE3DA75038777E979CFEC0C4BD19470E1CDC2F2986DCB242FB707F56332E753B0DB98E68C1089787C2F1DBB33F8E021C5289D6440D6561274FE6FF148601BFC9393A1A50A9DF1A11A27447806BF04912E9C2103C35E7BA8EC94332B4DAAEA0D79F9A21AD7E450957B1468D3BA44777E65E4F34B41080CE900D3BCB46EB6971A25146BD5BA91D0CACE1C8303B6210F1BCE649CCFD92ED1061CE8A468FE689C8E5DEE28C2D5CF71A88C1B3FD4282039B97290DE923DC5A02E0CE1C6F6EAF54504B227A44183C194A799CF570FB017D6A52BB88DFF862C0FDB317DFDB5B3A4C579A9900234705A0CD878A6A23F1E9064BCB158E92D7E468755F3CE96D2CD9240E93E96BEFC67342236F4BB7FE5435A592F0956DF270D989C21C09635EC65AC9B2FB42ADABD6A489E3A8ADFBF13BC55E967E72BAA5CDCC8504F5AD5EE180CCFF568F0CBCCF3302FED290DB4511AD811269CF41EC9CAE0E5B92B154F1C6D5D2384DF629CFAA00DAC0547E2FD37CFEE3DAD7D5A033F637CCCDAE534DE009E6922A3D87D61776664652885CA55EB39AABBBABEC66A9CD71822D485F3DC0A0F6DD685925BF2634E48853C22CC07CB11A3F5EB93D07DBB98497633401E8EA1607B03F0C77D803EF7E61FD221FC0B23A853624D92F95D6065E78B2EC47AC9023C1DCC06B27C99E6049B5FE67F64B9130E741765C18ADA9BEF7296F4AEB5C745E194CA92DBBD602F0F436C60CF1E8E62D01F95ECD9FCBA04F6F3CB5C1BF7E39078800A7A766BE5E244AD3FCE29E39839CFE82C9AAABF27CCF2FC653562D938F"
    expected_ciphertext_hex = "4D5D2B4BBF29EF93624317300F47767CA3A82A0AF01CCD63F257406429EF31EE396B6713760BBB84B40544A940C69010AD11C6070D32C0FA8D2ABC60C50D51F3E606C50954F260CFBB0BFD1D97D74375E626B87E059B42FCDFBEE2081EA020703B63CE0D76E8CA052719DBA0DB92B4FE5990ABBA62857A1FAA1963FF63FA12B23F3F7210F2C52C8029500943D6743F233187D7E3989CF8032F86D3F43B5256F5C250BAC00827455ED854F7DD05C75F1A7CB33F571C1F76E20D4CF912E70CE4BD4A759448EADD61119BFE270F8B3CA5EB804A5480FC1F44E84B01F26D76BAB86EFF75EBAE658AF2F58A8C3E625AF331B239345F65AF6321EBCD45DC187AE04E69AB7288026C1CD0C686379133B6620077C95C59F89C84510353512C2D32DC92C0141256D4B6E24C5744C2BF866657E55209F57A0633CEC6443EBD0F91A9FE54C4431A9B97CFF440E17D074FB0B3E0CBD64704B4508D17854B3A91AF70745B5F2C0AAB685919420CDD504860D414AE75D91FD29D0E9E8324A9D0E1448BCB2C7D1C25126DC7259458D8F0522ACA25B7176A15B5386663FA63558981ED8C3675E46B851727C8045757D1253D2A1E18478346726249464C0BE34DA715985D76532CB4C7D4B9A2B3D6F8086B547028997EA8EB7EE48B532EB8D9507BE3E80415D3D8F02B8BBF34EE56FA399F1B0E7ED52B00B7F66B9813E4D0A331988A731D411195C011970E529E4D35CA86143650B6820A05A3D606E6721E43062759640D404327C9285B9F66FD958D6CAD39449BF415213644BEC525D86D5261F2D1D12B84B32DE739A0F08D750FA20CD1F84A0749090EB2A79F9562F8D5CD1CC648113C1E98E9F626432DDEC5C57B4B17FFF771D7E754B9B0188F0BB8700B28CC971DCBAAB8E4C056F4248CEE971830357B8531D766E2EB958D493378AC241D05120BC8054E67B750A4D8168378D7281ED674CB16F4F4A1B45A5D3C049FF2EA525B4A491F5C717C114C6040773631CC55295410232D47588D745AF6F3669A11E9EE31C7C55A1412305A3D287DDFF2591DA75A860F8B26893BBD998772EDD7DB5713F40BD84B5CC61BFAC882CFE45B0BB8C36F1D518247DF726CA69BDC9B5E7E9CCC407997E3C07287A703DAECE78B7022B42957CA3EBA5919CF8F6C441ED0BC574FB475DC77E71F3E690B98C614FB5F4915BFEB005FCBA3BAB680E1C94495A4B8D1AB1500C4876C19322C78B85E693C36976DF34DE3F216EC0ED1A8BEF3FA5257AC5F3946093406EEC4BFAE7C751AA2212503327B8F0F0B8B27B3B73D19144A7C21DA284D59678DCD7115065B43939FFDDD4716E5885910C62630A31D5028DC04DE34B5B8D7FFC905041218FEB0FDD04C235190E62045F872EF2E21D51AA4EE8FADD182E0EE631D135E535407E90AFA3224F69236E4A3BFEE239A9F501DA2D8078507FD21EECE525E4FB4E64640F1D995DD3C269360418BFF88EE926566308DFA55EA1DB77731D2EB54B29B8C7AC8295E4A2FE927C50DC0BBDDA62DE85E09C73A1CBE622D7E190C"

    m_bytes = bytes.fromhex(m_hex)
    seed_sp_bytes = bytes.fromhex(seed_sp_hex)
    pk_bytes = bytes.fromhex(pk_hex)
    ciphertext = np.array([0] * (SABER_BYTES_CCA_DEC), dtype=np.uint8) #TODO: Check the size, it should be 1088 but couldnt get other way to initialize
    indcpa_kem_enc(m_bytes, seed_sp_bytes, pk_bytes, ciphertext)

    result_cipher = ""
    for i in ciphertext:
        result_cipher += f"{i:02x}"
    assert result_cipher.lower() == expected_ciphertext_hex.lower(), f"Expected {expected_ciphertext_hex}, but got {result_cipher}"

def test_indcpa_kem_dec():
    
    rng_init()

    sk_hex = "01E0FF030000E0FF0540000000FF3F00008000E0FFFFFF00F8FFFEBFFFFFFF0110000400000800024000FC7F000000FE7F000000FE1F00F07F00100000C0FF0700FF3F000000FFDFFF0180FFEFFFFFFFFFFF7F00F0FFFFBFFF0F00000000FCFFFF0F000240001000002000040001F0FF0100000000012000048001100002C0FFFFFFFD3F00FCFF00F0FF0180FF0F00FF3F00F87F00E0FFFD7F0000000000000080001000FEFFFF0700010000FCFF001000FABFFF070003C0FF030001E0FF0140001800002000048000F0FFFBBFFF0700FE1F000480FFFFFFFD7F000000FF5F00FC7F0040000280FF1F00FF5F00040001300000C0FF070000C0FFFF7F00F0FF018000F8FF012000F8FFFFDFFF0180000000020000088000E0FFFFBFFF070000E0FF0F00FF0F000080FF0F000120000400000000008000F8FFFF3F00008000F0FF0300000800FDDFFF030000E0FFFFFFFF0700012000FCFF0010000480FFF7FF01C0FF0B0000E0FF03C0FF0700FFFFFF0780FFEFFF0580FF0F000100000080FF0F00FEFFFF0F00022000FC7F00100004C0FF0F000220000480FF0F0000C0FF0F00FF1F00008000F0FF010000080003E0FF07000010000080FF0F00012000F8FFFF2F00FE7FFF0F00FF3F0000000010000680FFEFFF0000000080FF0F00FC3F00080000000000000010000400000800FD1F00FC7F01E0FFFDBF000800014000080000E0FF010000F0FF0120000400011000024000F0FF0020000880FF2F0004C0FFFFFFFF7F00000000E0FF03000000000020000080000000FEFFFF0700012000FCFFFF0F00FCBF00F8FFFE1F00FC7F0120000000000000000000FC7F000000020000F8FF0000000880001000FE7F000800006000FCFF003000FEFFFF1700000000040000F0FF070000F0FFFE1F00F87F011000FABF00080001E0FF0300000000FE7F000800FE5F000880FF3F0002000000000220000400FFFFFF034000000000E0FF0780FFDFFF05C0FFF7FFFFDFFF0780FE1F0002800000000120000000001000FEFFFFFFFF01200000800110000000000000FF1F000880FFEFFF03C0FF17000040000880001000FA3F000800000000000001000002400010000000000480000000FEFFFF0F00004000F87F02F0FFFDFFFFF7FF00E0FF0B80001000FE3F00F0FFFE1F000880FF0F00FCBFFFF7FF0040000080FFFFFFFF7F0000000260000000FF1F00FABF001000012000FCFFFFFFFF01000000000000000480001000FCBFFFFFFF004000F4FF0000000240000800FFFFFF0780FE2F00FEFFFFF7FFFF5F000000FF1F0002C0FF0F00FCFFFF0700011000000000F8FF010000040000E0FF0340FF0F00010000FC7FFF1F00FEBF00F8FFFE1F000800FF0F00FE3F0008000180FF0B80FFEFFF0340000800010000FCFFFF0F00FEBFFF0700FE3F000C0000E0FF050000F8FF00E0FF0380FFEFFF0580FFFFFFFF5F00F87F00D0FFFF3F00E8FF012000FCFFFF0F0000C0FFF7FFFE3F00F4FF00E0FFFDFFFFFFFF01E0FF0380000000000000F8FF002000088000F0FF0740000800012000F87F00E0FFFF3F00F0FFFEFFFFFFFFFF1F00004000F8FF012000040000F0FF0140000800FF3F00FC7F0110000400000800FE3F000400001000020000F0FF0220000000013000FE7F00000000200004800010000080000000FF3F00F87F011000FE3F00080000C0FFFFFFFFEFFFFDFFFFF7FF020000FC7FFF0F00FCFFFF0F00FFFFFF070000F0FFFD7F001000"
    ciphertext_hex = "4D5D2B4BBF29EF93624317300F47767CA3A82A0AF01CCD63F257406429EF31EE396B6713760BBB84B40544A940C69010AD11C6070D32C0FA8D2ABC60C50D51F3E606C50954F260CFBB0BFD1D97D74375E626B87E059B42FCDFBEE2081EA020703B63CE0D76E8CA052719DBA0DB92B4FE5990ABBA62857A1FAA1963FF63FA12B23F3F7210F2C52C8029500943D6743F233187D7E3989CF8032F86D3F43B5256F5C250BAC00827455ED854F7DD05C75F1A7CB33F571C1F76E20D4CF912E70CE4BD4A759448EADD61119BFE270F8B3CA5EB804A5480FC1F44E84B01F26D76BAB86EFF75EBAE658AF2F58A8C3E625AF331B239345F65AF6321EBCD45DC187AE04E69AB7288026C1CD0C686379133B6620077C95C59F89C84510353512C2D32DC92C0141256D4B6E24C5744C2BF866657E55209F57A0633CEC6443EBD0F91A9FE54C4431A9B97CFF440E17D074FB0B3E0CBD64704B4508D17854B3A91AF70745B5F2C0AAB685919420CDD504860D414AE75D91FD29D0E9E8324A9D0E1448BCB2C7D1C25126DC7259458D8F0522ACA25B7176A15B5386663FA63558981ED8C3675E46B851727C8045757D1253D2A1E18478346726249464C0BE34DA715985D76532CB4C7D4B9A2B3D6F8086B547028997EA8EB7EE48B532EB8D9507BE3E80415D3D8F02B8BBF34EE56FA399F1B0E7ED52B00B7F66B9813E4D0A331988A731D411195C011970E529E4D35CA86143650B6820A05A3D606E6721E43062759640D404327C9285B9F66FD958D6CAD39449BF415213644BEC525D86D5261F2D1D12B84B32DE739A0F08D750FA20CD1F84A0749090EB2A79F9562F8D5CD1CC648113C1E98E9F626432DDEC5C57B4B17FFF771D7E754B9B0188F0BB8700B28CC971DCBAAB8E4C056F4248CEE971830357B8531D766E2EB958D493378AC241D05120BC8054E67B750A4D8168378D7281ED674CB16F4F4A1B45A5D3C049FF2EA525B4A491F5C717C114C6040773631CC55295410232D47588D745AF6F3669A11E9EE31C7C55A1412305A3D287DDFF2591DA75A860F8B26893BBD998772EDD7DB5713F40BD84B5CC61BFAC882CFE45B0BB8C36F1D518247DF726CA69BDC9B5E7E9CCC407997E3C07287A703DAECE78B7022B42957CA3EBA5919CF8F6C441ED0BC574FB475DC77E71F3E690B98C614FB5F4915BFEB005FCBA3BAB680E1C94495A4B8D1AB1500C4876C19322C78B85E693C36976DF34DE3F216EC0ED1A8BEF3FA5257AC5F3946093406EEC4BFAE7C751AA2212503327B8F0F0B8B27B3B73D19144A7C21DA284D59678DCD7115065B43939FFDDD4716E5885910C62630A31D5028DC04DE34B5B8D7FFC905041218FEB0FDD04C235190E62045F872EF2E21D51AA4EE8FADD182E0EE631D135E535407E90AFA3224F69236E4A3BFEE239A9F501DA2D8078507FD21EECE525E4FB4E64640F1D995DD3C269360418BFF88EE926566308DFA55EA1DB77731D2EB54B29B8C7AC8295E4A2FE927C50DC0BBDDA62DE85E09C73A1CBE622D7E190C"
    input_m_hex = "730FE20A3919F215DA05D80EF907A11A1F0FF01CF41E4809E000381D80023312"
    expected_m_hex = "3BD09B6EA5E37E540373187B7A91F74856573540E753715644B84276FEFF1765"

    sk_bytes = np.frombuffer(bytes.fromhex(sk_hex), dtype=np.uint8).copy()
    ciphertext_bytes = np.frombuffer(bytes.fromhex(ciphertext_hex), dtype=np.uint8).copy()
    res_m = np.frombuffer(bytes.fromhex(input_m_hex), dtype=np.uint8).copy()

    indcpa_kem_dec(sk_bytes, ciphertext_bytes, res_m)

    result_m = ""
    for i in res_m:
        result_m += f"{i:02x}"

    assert result_m.lower() == expected_m_hex.lower(), f"Expected {expected_m_hex}, but got {result_m}"

test_indcpa_kem_dec()