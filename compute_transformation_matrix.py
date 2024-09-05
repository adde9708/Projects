from math import cos, isinf, isnan, pi, sin, sqrt


def normalize_vector(vec):
    magnitude = sqrt(sum(x**2 for x in vec))

    if magnitude > 0.0:
        normalized_vector = [x / magnitude for x in vec]

        return normalized_vector

    normalized_vector = [1.0, 0.0, 0.0]

    return normalized_vector


def sanitize_value(value):
    return value if not isnan(value) or not isinf(value) else 0.0


def calculate_matrix_product(product, matrix1, matrix2):
    # Get the dimensions of the input matrices
    rows_matrix1 = len(matrix1)
    cols_matrix1 = len(matrix1[0])
    rows_matrix2 = len(matrix2)
    cols_matrix2 = len(matrix2[0])

    # Ensure the matrices can be multiplied
    if cols_matrix1 != rows_matrix2:
        raise ValueError("Matrix1 columns must equal Matrix2 rows for multiplication")

    # Perform matrix multiplication
    for row in range(rows_matrix1):
        for col in range(cols_matrix2):
            value = sum(matrix1[row][k] * matrix2[k][col] for k in range(cols_matrix1))
            product[row][col] = sanitize_value(value)

    # Convert the product matrix to a tuple of tuples
    product = tuple(tuple(row) for row in product)

    return product


def rotate_and_transform_matrix(product, input_matrix, angle):

    angle = min(angle, 65535)
    angle_radians = angle * pi / 180.0
    sine = sin(angle_radians)
    cosine = cos(angle_radians)

    rotation_matrix = [
        [cosine, -sine, 0.0, 0.0],
        [sine, cosine, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

    product = calculate_matrix_product(product, input_matrix, rotation_matrix)

    return product


def sanitize_vector(vector):
    santized_vector = [sanitize_value(x) for x in vector]
    return santized_vector


def cross_product(a, b):
    product = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]
    return product


def get_direction(position_start, position_end):

    direction = [position_end[i] - position_start[i] for i in range(3)]
    direction = normalize_vector(direction)
    return direction


def get_custom_params():
    params = [1, 2, 3]
    return params


def check_custom_params_availability(params):
    return True


def get_custom_data(params):
    return sum(params)


def get_direction_vector(data_ptr):
    direction_vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    return direction_vectors[data_ptr % 2]


def get_custom_data_from_context(context):
    return context % 128


def compute_transformation_matrix(
    context,
    position_start,
    position_end,
    rotation_angle,
    use_default_rotation,
    use_custom_direction,
):
    default_up = [0.0, 0.0, 1.0]
    direction = get_direction(position_start, position_end)
    if use_default_rotation:
        params = get_custom_params()
        params_available = check_custom_params_availability(params)
        if params_available:
            custom_data_ptr = get_custom_data(params)
            direction_vector = get_direction_vector(custom_data_ptr)
            default_up = sanitize_vector(direction_vector)
    elif use_custom_direction:
        custom_data_ptr = get_custom_data_from_context(context)
        direction_vector = get_direction_vector(custom_data_ptr)
        default_up = sanitize_vector(direction_vector)

    right_vector = cross_product(default_up, direction)
    right_vector = normalize_vector(right_vector)
    up_vector = cross_product(direction, right_vector)
    up_vector = normalize_vector(up_vector)

    result_matrix = [
        right_vector + [0.0],
        up_vector + [0.0],
        direction + [0.0],
        position_start + [1.0],
    ]

    result_matrix = rotate_and_transform_matrix(
        result_matrix, result_matrix, rotation_angle
    )
    return result_matrix


def main():
    position_start = [0.0, 0.0, 0.0]
    position_end = [1.0, 1.0, 1.0]
    rotation_angle = 256
    use_default_rotation = True
    use_custom_direction = False

    result_matrix = compute_transformation_matrix(
        12345,
        position_start,
        position_end,
        rotation_angle,
        use_default_rotation,
        use_custom_direction,
    )

    # Print the resulting matrix
    for row in result_matrix:
        print(" ".join(f"{value:.6f}" for value in row))


if __name__ == "__main__":
    main()
