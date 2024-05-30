import numpy as np

from pysaber.api import CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES
from pysaber.saber_indcpa import indcpa_kem_keypair
from pysaber.saber_params import (SABER_INDCPA_PUBLICKEYBYTES,
                                  SABER_INDCPA_SECRETKEYBYTES)
from tests.common import rng_init


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
