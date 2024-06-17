import argparse

from predictor import DepthEstimationModel


def main():
    parser = argparse.ArgumentParser(description="Depth Estimation CLI")

    # kullanılan argümanlar; image_path, output_path
    """
    argparse kullanımı:
    short , long, type, help şeklinde argumanlar tanımlanır.
    
    """
    parser.add_argument("-ip", "--image_path", type=str, help="Path to the image")
    parser.add_argument(
        "-op", "--output_path", type=str, help="Path to save the colored depth map"
    )


    args = parser.parse_args()

    #? DepthEstimationModel sınıfından model oluşturulur.
    model = DepthEstimationModel()

    result = model.calculate_depthmap(args.image_path, args.output_path)


if __name__ == "__main__":
    main()
