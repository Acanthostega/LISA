#version 130

uniform mat4 model;
uniform mat4 rotate;
uniform sampler2D map;
uniform vec3 camera;
uniform float materialShininess;
uniform vec3 materialSpecularColor;

uniform struct Light {
    vec4 position;
    vec3 intensities;
    float attenuation;
    float ambientCoefficient;
    // float coneAngle;
    // vec3 coneDirection;
} light;

in vec3 texcoord;
in vec3 fragNormal;

out vec4 finalColor;

vec3 ApplyLight(Light light, vec3 surfaceColor, vec3 normal, vec3 surfacePos, vec3 surfaceToCamera) {
    vec3 surfaceToLight;
    float attenuation = 1.0;
    if(light.position.w == 0.0) {
        //directional light
        surfaceToLight = normalize(light.position.xyz);
        attenuation = 1.0; //no attenuation for directional lights
    } else {
        //point light
        surfaceToLight = normalize(light.position.xyz - surfacePos);
        float distanceToLight = length(light.position.xyz - surfacePos);
        attenuation = 1.0 / (1.0 + light.attenuation * pow(distanceToLight, 2));

        //cone restrictions (affects attenuation)
        // float lightToSurfaceAngle = degrees(acos(dot(-surfaceToLight, normalize(light.coneDirection))));
        // if(lightToSurfaceAngle > light.coneAngle){
        //     attenuation = 0.0;
        // }
    }

    //ambient
    vec3 ambient = light.ambientCoefficient * surfaceColor.rgb * light.intensities;

    //diffuse
    float diffuseCoefficient = max(0.0, dot(normal, surfaceToLight));
    vec3 diffuse = diffuseCoefficient * surfaceColor.rgb * light.intensities;

    //specular
    float specularCoefficient = 0.0;
    if(diffuseCoefficient > 0.0)
        specularCoefficient = pow(max(0.0, dot(surfaceToCamera, reflect(-surfaceToLight, normal))), materialShininess);
    vec3 specular = specularCoefficient * materialSpecularColor * light.intensities;

    //linear color (color before gamma correction)
    return ambient + attenuation*(diffuse + specular);
}

void main()
{
    vec2 longitudeLatitude = vec2(
        (-atan(texcoord.y, texcoord.x) / 3.1415926 + 1.0) * 0.5,
        (asin(texcoord.z) / 3.1415926 + 0.5)
    );
    vec4 surfaceColor = texture2D(map, longitudeLatitude);

    vec3 fragPosition = mat3(model) * texcoord;

    vec3 surfaceToLight = vec3(light.position) - fragPosition;

    finalColor = vec4(ApplyLight(light, surfaceColor.rgb, fragNormal, fragPosition, normalize(camera-fragPosition)), 1);
}

