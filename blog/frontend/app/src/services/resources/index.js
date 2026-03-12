import { AuthResource } from "./auth.resource";
import { PostResource } from "./post.resource";

export default {
    auth: new AuthResource(),
    post: new PostResource(),
};
