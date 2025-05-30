from torch import nn



def get_activation(act_fn):
    if act_fn in ["swish", "silu"]:
        return nn.SiLU()
    elif act_fn == "mish":
        return nn.Mish()
    elif act_fn == "gelu":
        return nn.GELU()
    elif act_fn == "relu":
        return nn.ReLU()
    elif act_fn == "leaky_relu":
        return nn.LeakyReLU(negative_slope=0.01)
    else:
        raise ValueError(f"Unsupported activation function: {act_fn}")
