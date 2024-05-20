import cv2

class LabelDrawer:
    def __init__(self, font_scale=1.5, font_thickness=1, rectangle_thickness=1,
                 text_color=(255, 255, 255), rectangle_color=(0, 255, 0),
                 text_background_color=(0, 255, 0, 50)):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = font_scale
        self.font_thickness = font_thickness
        self.rectangle_thickness = rectangle_thickness
        self.text_color = text_color
        self.rectangle_color = rectangle_color
        self.text_background_color = text_background_color

    def draw_labels(self, img, labels):
        for label in labels:
            name = label['Name']
            confidence = label['Confidence']
            if 'Instances' in label:
                for instance in label['Instances']:
                    self._draw_label(img, name, confidence, instance)
        return img

    def _draw_label(self, img, name, confidence, instance):
        box = instance['BoundingBox']
        left = int(box['Left'] * img.shape[1])
        top = int(box['Top'] * img.shape[0])
        width = int(box['Width'] * img.shape[1])
        height = int(box['Height'] * img.shape[0])

        # Draw rectangle around the object
        cv2.rectangle(img, (left, top), (left + width, top + height), self.rectangle_color, self.rectangle_thickness)

        # Prepare text and background
        label_text = f"{name} ({confidence:.2f}%)"
        (text_width, text_height), _ = cv2.getTextSize(label_text, self.font, self.font_scale, self.font_thickness)

        # Draw semi-transparent rectangle as text background
        overlay = img.copy()
        cv2.rectangle(overlay, (left, top - text_height - 10), (left + text_width, top), self.text_background_color, -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)

        # Draw the text
        cv2.putText(img, label_text, (left, top - 5), self.font, self.font_scale, self.text_color, self.font_thickness)
