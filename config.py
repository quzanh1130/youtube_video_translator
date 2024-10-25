import torch

model_name_vn_to_en = "VietAI/envit5-translation"
model_name_en_to_vn = "vinai/vinai-translate-vi2en"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")