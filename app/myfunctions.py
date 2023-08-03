import requests
# from .models import Exercise

def getExercise(page):
    """
    Returns a list of exercises, each in a dict:
    {name, type, muscle, equipment, difficulty, instructions}
    """
    # k = index
    # offset = k // 10
    # new_k = k - 10*offset
    # print(k, offset, new_k)

    # 0 - 0-10
    # 1 - 10-20
    # 2 - 20-30
    # start = offset*10
    # stop = start + 10

    offset = page*10
    
    # for i in range(start, stop, 10):
    url = f"https://api.api-ninjas.com/v1/exercises?offset={offset}"
    api_key = "ka/g7nybqosAgLyFNCod1A==WBv07XT0PI2TrXTO"
    response = requests.get(url, headers={'X-Api-Key': api_key})
    data = response.json()
    return data    
        # for j in range(len(data)):
        #     name = data[j]["name"]
        #     tipo = data[j]["type"]
        #     muscle = data[j]["muscle"]
        #     equip = data[j]["equipment"]
        #     diff = data[j]["difficulty"]
        #     instruct = data[j]["instructions"]
            # exercise = Exercise(name, tipo, muscle, equip, diff, instruct)
            # exercise.addExercise()
            # print(name, tipo, muscle, equip, diff, instruct)

# print(getExercise(1))

def top4(arr):
        occurs = {}
        mx = 0
        for muscle in arr:
            if muscle not in occurs:
                occurs[muscle] = 1
                mx = max(mx, 1)
            else:
                occurs[muscle] += 1
                mx = max(mx, occurs[muscle])
        result = []
        for k, v in occurs.items():
            if v == mx:
                result.append(k)
            if len(result) == 4:
                return result
        for k, v in occurs.items():
            if v == mx-1:
                result.append(k)    
            if len(result) == 4:
                return result
        return result


def listToText(arr):
    "string objects only - takes list of string objects and formats them to 'a, b, c and d' style text list"
    if len(arr) == 1:
        return arr[0].capitalize()

    text_list = ", ".join(word.capitalize() for word in arr[:-1])
    text_list += f" and {arr[-1].capitalize()}"

    return text_list

def dashList(arr):
    "string or int or mixed list - converted to dash list"
    if len(arr) == 1:
        return arr[0]
    dash_list = "-".join([str(item) for item in arr])
    return dash_list



extra_exercies = [{'name': 'Flutter Kicks', 'type': 'strength', 'muscle': 'glutes', 'equipment': 'None', 'difficulty': 'intermediate', 'instructions': 'On a flat bench lie facedown with the hips on the edge of the bench, the legs straight with toes high off the floor and with the arms on top of the bench holding on to the front edge. Squeeze your glutes and hamstrings and straighten the legs until they are level with the hips. This will be your starting position. Start the movement by lifting the left leg higher than the right leg. Then lower the left leg as you lift the right leg. Continue alternating in this manner (as though you are doing a flutter kick in water) until you have done the recommended amount of repetitions for each leg. Make sure that you keep a controlled movement at all times. Tip: You will breathe normally as you perform this movement.  Variations: As you get more advanced you can use ankle weights.'},
{'name': 'Superman', 'type': 'stretching', 'muscle': 'lower_back', 'equipment': 'body_only', 'difficulty': 'intermediate', 'instructions': 'To begin, lie straight and face down on the floor or exercise mat. Your arms should be fully extended in front of you. This is the starting position. Simultaneously raise your arms, legs, and chest off of the floor and hold this contraction for 2 seconds. Tip: Squeeze your lower back to get the best results from this exercise. Remember to exhale during this movement. Note: When holding the contracted position, you should look like superman when he is flying. Slowly begin to lower your arms, legs and chest back down to the starting position while inhaling. Repeat for the recommended amount of repetitions prescribed in your program.  Variations: You can also perform this exercise using one arm and leg at a time. Simply elevating your left leg, arm and side of your chest and do the same with the right side.'},
{'name': 'Glute Kickback', 'type': 'strength', 'muscle': 'glutes', 'equipment': 'body_only', 'difficulty': 'beginner', 'instructions': 'Kneel on the floor or an exercise mat and bend at the waist with your arms extended in front of you (perpendicular to the torso) in order to get into a kneeling push-up position but with the arms spaced at shoulder width. Your head should be looking forward and the bend of the knees should create a 90-degree angle between the hamstrings and the calves. This will be your starting position. As you exhale, lift up your right leg until the hamstrings are in line with the back while maintaining the 90-degree angle bend. Contract the glutes throughout this movement and hold the contraction at the top for a second. Tip: At the end of the movement the upper leg should be parallel to the floor while the calf should be perpendicular to it. Go back to the initial position as you inhale and now repeat with the left leg. Continue to alternate legs until all of the recommended repetitions have been performed.  Variations: For this exercise you can also perform all of the repetitions with one leg first and then the other one. Additionally, you can also add ankle weights.'},
{'name': 'Exercise ball weighted hyperextension', 'type': 'strength', 'muscle': 'lower_back', 'equipment': 'exercise_ball', 'difficulty': 'beginner', 'instructions': 'To begin, lie down on an exercise ball with your torso pressing against the ball and parallel to the floor. The ball of your feet should be pressed against the floor to help keep you balanced. Place a weighted plate under your chin or behind your neck. This is the starting position. Slowly raise your torso up by bending at the waist and lower back. Remember to exhale during this movement. Hold the contraction on your lower back for a second and lower your torso back down to the starting position while inhaling. Repeat for the recommended amount of repetitions prescribed in your program.  Caution: If you are new to this exercise, it is best to perform this exercise without any weights until you develop good form. Variations: You can use a regular hyperextension bench also or perform on a flat bench with someone holding your legs.'},
{'name': 'Barbell behind-the-back shrug', 'type': 'strength', 'muscle': 'traps', 'equipment': 'barbell', 'difficulty': 'intermediate', 'instructions': 'Stand up straight with your feet at shoulder width as you hold a barbell with both hands behind your back using a pronated grip (palms facing back). Tip: Your hands should be a little wider than shoulder width apart. You can use wrist wraps for this exercise for better grip. This will be your starting position. Raise your shoulders up as far as you can go as you breathe out and hold the contraction for a second. Tip: Refrain from trying to lift the barbell by using your biceps. The arms should remain stretched out at all times. Slowly return to the starting position as you breathe in. Repeat for the recommended amount of repetitions.  Variations: You can also rotate your shoulders as you go up, going in a semicircular motion from rear to front. However this version is not good for people with shoulder problems. In addition, this exercise can be performed with the barbell in front of your thighs, with dumbbells by the side, a smith machine or with a shrug machine.'},
{'name': 'Rack pull', 'type': 'powerlifting', 'muscle': 'lower_back', 'equipment': 'barbell', 'difficulty': 'intermediate', 'instructions': 'Set up in a power rack with the bar on the pins. The pins should be set to the desired point; just below the knees, just above, or in the mid thigh position. Position yourself against the bar in proper deadlifting position. Your feet should be under your hips, your grip shoulder width, back arched, and hips back to engage the hamstrings. Since the weight is typically heavy, you may use a mixed grip, a hook grip, or use straps to aid in holding the weight. With your head looking forward, extend through the hips and knees, pulling the weight up and back until lockout. Be sure to pull your shoulders back as you complete the movement. Return the weight to the pins and repeat.'},
{'name': 'Seated Back Extension', 'type': 'strength', 'muscle': 'lower_back', 'equipment': 'machine', 'difficulty': 'beginner', 'instructions': 'Adjust the machine and select an appropriate load. Seat yourself with your upper back against the roller and grasp the handles with your feet planted firmly on the footrest. Your head should remain looking forward and your chest should be up. This will be your starting position. Initiate the movement by extending at the hips and lumbar spine to straighten your body, pushing the roller to the rear. At the top of the motion pause, and then return to the starting position.'},
{'name': 'Iliotibial band SMR', 'type': 'stretching', 'muscle': 'abductors', 'equipment': 'foam_roll', 'difficulty': 'intermediate', 'instructions': 'Lay on your side, with the bottom leg placed onto a foam roller between the hip and the knee. The other leg can be crossed in front of you. Place as much of your weight as is tolerable onto your bottom leg; there is no need to keep your bottom leg in contact with the ground. Be sure to relax the muscles of the leg you are stretching. Roll your leg over the foam from you hip to your knee, pausing for 10-30 seconds at points of tension. Repeat with the opposite leg.'},
{'name': 'Thigh abductor', 'type': 'strength', 'muscle': 'abductors', 'equipment': 'machine', 'difficulty': 'intermediate', 'instructions': 'To begin, sit down on the abductor machine and select a weight you are comfortable with. When your legs are positioned properly, grip the handles on each side. Your entire upper body (from the waist up) should be stationary. This is the starting position. Slowly press against the machine with your legs to move them away from each other while exhaling. Feel the contraction for a second and begin to move your legs back to the starting position while breathing in. Note: Remember to keep your upper body stationary to prevent any injuries from occurring. Repeat for the recommended amount of repetitions.'},
{'name': 'Standing barbell calf raise', 'type': 'strength', 'muscle': 'calves', 'equipment': 'barbell', 'difficulty': 'beginner', 'instructions': 'This exercise is best performed inside a squat rack for safety purposes. To begin, first set the bar on a rack that best matches your height. Once the correct height is chosen and the bar is loaded, step under the bar and place the bar on the back of your shoulders (slightly below the neck). Hold on to the bar using both arms at each side and lift it off the rack by first pushing with your legs and at the same time straightening your torso. Step away from the rack and position your legs using a shoulder width medium stance with the toes slightly pointed out. Keep your head up at all times as looking down will get you off balance and also maintain a straight back. The knees should be kept with a slight bend; never locked. This will be your starting position. Tip: For better range of motion you may also place the ball of your feet on a wooden block but be careful as this option requires more balance and a sturdy block. Raise your heels as you breathe out by extending your ankles as high as possible and flexing your calf. Ensure that the knee is kept stationary at all times. There should be no bending at any time. Hold the contracted position by a second before you start to go back down. Go back slowly to the starting position as you breathe in by lowering your heels as you bend the ankles until calves are stretched. Repeat for the recommended amount of repetitions.  Caution: If you suffer from lower back problems, a better exercise is the calf press as during a standing calf raise the back has to support the weight being lifted. Also, maintain your back straight and stationary at all times. Rounding of the back can cause lower back injury. Variations: There are several other ways to perform a standing calf raise. A calf press machine instead of a squat rack can be used as well as dumbbells with one leg or two legs at a time. A smith machine can be used for calf raises as well. You can also perform the barbell calf raise using a piece of wood to place the ball of the foot. This will allow you to get a better range of motion. However be cautious as in this case you will need to balance yourself much better.'},
{'name': 'Cable straight-bar upright row', 'type': 'strength', 'muscle': 'traps', 'equipment': 'cable', 'difficulty': 'intermediate', 'instructions': "Grasp a straight bar cable attachment that is attached to a low pulley with a pronated (palms facing your thighs) grip that is slightly less than shoulder width. The bar should be resting on top of your thighs. Your arms should be extended with a slight bend at the elbows and your back should be straight. This will be your starting position. Use your side shoulders to lift the cable bar as you exhale. The bar should be close to the body as you move it up. Continue to lift it until it nearly touches your chin. Tip: Your elbows should drive the motion. As you lift the bar, your elbows should always be higher than your forearms. Also, keep your torso stationary and pause for a second at the top of the movement. Lower the bar back down slowly to the starting position. Inhale as you perform this portion of the movement. Repeat for the recommended amount of repetitions.  Caution: Be very careful with how much weight you use in this exercise. Too much weight leads to bad form, which in turn can cause shoulder injury. I've seen this too many times so please no jerking, swinging and cheating. Also, if you suffer from shoulder problems, you may want to stay away from upright rows and substitute by some form of lateral raises. Variations: This exercise can also be performed using a straight or e-z bar. Another variation is to use dumbbells, though this later exercise should be reserved by the most advanced people that are well familiarized with correct execution."},
{'name': 'Seated Good Mornings', 'type': 'powerlifting', 'muscle': 'lower_back', 'equipment': 'barbell', 'difficulty': 'beginner', 'instructions': 'Set up a box in a power rack. The pins should be set at an appropriate height. Begin by stepping under the bar and placing it across the back of the shoulders, not on top of your traps. Squeeze your shoulder blades together and rotate your elbows forward, attempting to bend the bar across your shoulders. Remove the bar from the rack, creating a tight arch in your lower back. Keep your head facing forward. With your back, shoulders, and core tight, push your knees and butt out and you begin your descent. Sit back with your hips until you are seated on the box. This will be your starting position. Keeping the bar tight, bend forward at the hips as much as possible. If you set the pins to what would be parallel, you not only have a safety if you fail, but know when to stop. Pause just above the pins and reverse the motion until your torso it upright.'},
{'name': 'Stiff Leg Barbell Good Morning', 'type': 'strength', 'muscle': 'lower_back', 'equipment': 'barbell', 'difficulty': 'beginner', 'instructions': 'This exercise is best performed inside a squat rack for safety purposes. To begin, first set the bar on a rack that best matches your height. Once the correct height is chosen and the bar is loaded, step under the bar and place the back of your shoulders (slightly below the neck) across it. Hold on to the bar using both arms at each side and lift it off the rack by first pushing with your legs and at the same time straightening your torso. Step away from the rack and position your legs using a shoulder width medium stance. Keep your head up at all times as looking down will get you off balance and also maintain a straight back. This will be your starting position. Keeping your legs stationary, move your torso forward by bending at the hips while inhaling. Lower your torso until it is parallel with the floor. Begin to raise the bar as you exhale by elevating your torso back to the starting position. Repeat for the recommended amount of repetitions.  Caution: This is not an exercise to be taken lightly. Be cautious with the weight used; in case of doubt, use less weight rather than more. The stiff-legged barbell good morning is a very safe exercise but only if performed properly.'},
{'name': 'Fire Hydrant', 'type': 'strength', 'muscle': 'abductors', 'equipment': 'body_only', 'difficulty': 'beginner', 'instructions': 'Position yourself on your hands and knees on the ground. This will be your starting position. Keeping the knee in a bent position, abduct the femur, moving your knee away from the midline of the body. Pause at the top of the motion, and then slowly return to the starting position. Perform this slowly for a number of repetitions, and repeat on the other side.'},
{'name': 'Windmills', 'type': 'stretching', 'muscle': 'abductors', 'equipment': 'body_only', 'difficulty': 'intermediate', 'instructions': 'Lie on your back with your arms extended out to the sides and your legs straight. This will be your starting position. Lift one leg and quickly cross it over your body, attempting to touch the ground near the opposite hand. Return to the starting position, and repeat with the opposite leg. Continue to alternate for 10-20 repetitions.'},
{'name': 'Cable shrug', 'type': 'strength', 'muscle': 'traps', 'equipment': 'cable', 'difficulty': 'intermediate', 'instructions': 'Grasp a cable bar attachment that is attached to a low pulley with a shoulder width or slightly wider overhand (palms facing down) grip. Stand erect close to the pulley with your arms extended in front of you holding the bar. This will be your starting position. Lift the bar by elevating the shoulders as high as possible as you exhale. Hold the contraction at the top for a second. Tip: The arms should remain extended at all times. Refrain from using the biceps to help lift the bar. Only the shoulders should be moving up and down. Lower the bar back to the original position. Repeat for the recommended amount of repetitions.  Variations: You can perform this exercise with bands, barbells or dumbbell. You can also use a single handle and work one side at a time.'},
{'name': 'Smith machine behind-the-back shrug', 'type': 'strength', 'muscle': 'traps', 'equipment': 'machine', 'difficulty': 'intermediate', 'instructions': 'With the bar at thigh level, load an appropriate weight. Stand with the bar behind you, taking a shoulder-width, pronated grip on the bar and unhook the weight. You should be standing up straight with your head and chest up and your arms extended. This will be your starting position. Initiate the movement by shrugging your shoulders straight up. Do not flex the arms or wrist during the movement. After a brief pause return the weight to the starting position. Repeat for the desired number of repetitions before engaging the hooks to rack the weight.'},
{'name': 'Upright Row - With Bands', 'type': 'strength', 'muscle': 'traps', 'equipment': 'bands', 'difficulty': 'beginner', 'instructions': "To begin, stand on an exercise band so that tension begins at arm's length. Grasp the handles using a pronated (palms facing your thighs) grip that is slightly less than shoulder width. The handles should be resting on top of your thighs. Your arms should be extended with a slight bend at the elbows and your back should be straight. This will be your starting position. Use your side shoulders to lift the handles as you exhale. The handles should be close to the body as you move them up. Continue to lift the handles until they nearly touches your chin. Tip: Your elbows should drive the motion. As you lift the handles, your elbows should always be higher than your forearms. Also, keep your torso stationary and pause for a second at the top of the movement. Lower the handles back down slowly to the starting position. Inhale as you perform this portion of the movement. Repeat for the recommended amount of repetitions.  Variations: This exercise can also be performed using a straight or e-z bar. Another variation is to use dumbbells, though this later exercise should be reserved by the most advanced people that are well familiarized with correct execution."},
{'name': 'Exercise ball hip thrust', 'type': 'strength', 'muscle': 'glutes', 'equipment': 'exercise_ball', 'difficulty': 'intermediate', 'instructions': 'Lay on a ball so that your upper back is on the ball with your hips unsupported. Both feet should be flat on the floor, hip width apart or wider. This will be your starting position. Begin by extending the hips using your glutes and hamstrings, raising your hips upward as you bridge. Pause at the top of the motion and return to the starting position.'},
{'name': 'Side Leg Raises', 'type': 'stretching', 'muscle': 'adductors', 'equipment': 'body_only', 'difficulty': 'beginner', 'instructions': 'Stand next to a chair, which you may hold onto as a support. Stand on one leg. This will be your starting position. Keeping your leg straight, raise it as far out to the side as possible, and swing it back down, allowing it to cross the opposite leg. Repeat this swinging motion 5-10 times, increasing the range of motion as you do so.'},
{'name': 'Kneeling Jump Squat', 'type': 'olympic_weightlifting', 'muscle': 'glutes', 'equipment': 'barbell', 'difficulty': 'beginner', 'instructions': 'Begin kneeling on the floor with a barbell racked across the back of your shoulders, or you can use your body weight for this exercise. This can be done inside of a power rack to make unracking easier. Sit back with your hips until your glutes touch your feet, keeping your head and chest up. Explode up with your hips, generating enough power to land with your feet flat on the floor. Continue with the squat by driving through your heels and extending the knees to come to a standing position.'}]
