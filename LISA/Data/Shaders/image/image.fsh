#version 150 core

in vec2 coordTexture;

uniform bool fbo;
uniform sampler2D tex;

out vec4 out_Color;

vec2 inverted_y;

void main()
{
    if (!fbo) {
        out_Color = texture(tex, coordTexture);
    } else {
        inverted_y = coordTexture;
        inverted_y.y = 1. - inverted_y.y;
        out_Color = texture(tex, inverted_y);
    }
}
