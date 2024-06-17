import torch
from PIL import Image

from misc import colorize


class DepthEstimationModel:
    def __init__(self) -> None:
        """
        self.device: "cuda" mı yoksa "cpu" mu olduğunu belirler.
        self.model: Modeli yükler ve self.device üzerinde çalıştırır.
        """

        self.device = self._get_device()
        self.model = self._initialize_model(
            model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"
        ).to(self.device)

    def _get_device(self):
        """Eğer cuda kullanılabilirse cuda, değilse cpu döndürür."""

        return "cuda" if torch.cuda.is_available() else "cpu"

    def _initialize_model(self, model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"):
        """
        Modeli yükler ve döndürür.
        torch.hub.load(github_repo, model_name, pretrained=True) ile model yüklenir.

        """
        torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=True)
        model = torch.hub.load(
            model_repo, model_name, pretrained=True, skip_validation=False
        )
        model.eval()
        print(f"Model initialized. and using {self.device}")
        return model

    def save_colored_depth(self, depth_numpy, output_path):
        """
        depth_numpy: Depth map olarak numpy array.
        output_path: Kaydedilecek dosyanın yolu.
        """
        colored = colorize(depth_numpy)
        Image.fromarray(colored).save(output_path)
        print("Image saved.")

    def calculate_depthmap(self, image_path, output_path):
        """
        image_path: Derinlik haritası hesaplanacak resmin yolu.
        output_path: Kaydedilecek dosyanın yolu.
        """

        image = Image.open(image_path).convert("RGB")
        print("Image read.")

        depth_numpy = self.model.infer_pil(image)
        self.save_colored_depth(depth_numpy, output_path)
        return f"Image saved to {output_path}"



