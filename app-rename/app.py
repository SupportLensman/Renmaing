from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def rename_student_images(root_path):
    renamed_count = 0
    for class_folder in os.listdir(root_path):
        class_path = os.path.join(root_path, class_folder)
        if os.path.isdir(class_path):
            for student_folder in os.listdir(class_path):
                student_path = os.path.join(class_path, student_folder)
                if os.path.isdir(student_path):
                    image_count = 0
                    for image in os.listdir(student_path):
                        if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            image_count += 1
                            old_path = os.path.join(student_path, image)
                            new_name = f"{class_folder}-{student_folder}"
                            if image_count > 1:
                                new_name += f"_{image_count}"
                            new_name += os.path.splitext(image)[1]
                            new_path = os.path.join(student_path, new_name)
                            os.rename(old_path, new_path)
                            renamed_count += 1
    return renamed_count

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rename', methods=['POST'])
def rename():
    root_path = request.form['path']
    if os.path.exists(root_path):
        renamed_count = rename_student_images(root_path)
        return jsonify({"success": True, "message": f"Renamed {renamed_count} images successfully."})
    else:
        return jsonify({"success": False, "message": "The specified path does not exist."})

if __name__ == '__main__':
    app.run(debug=True)
